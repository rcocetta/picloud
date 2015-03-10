import json
import sys
import logging
import os
from os import listdir
from datetime import datetime
from datetime import date



LOG_FORMAT = "%(asctime)-15s - [PiCloudMain][%(levelname)s] - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logging.getLogger("picloud")

class PiCloudSync:
	CFG = None

	dateFormat = "%Y-%m-%d %H:%M:%S"
	def __init__(self, cfg):
		self.CFG = cfg
	def checkIs(self, role, path, sign='', filename='picloud.json'):
		"""
		Checks that the specified path contains a "role".
		path --> the path you want to check
		role --> the role you want to check
		sign --> an optional signature which will be checked

		"""
		filename = path + "/" + filename
		try:
			f = open(filename, 'r')
			info = json.load(f)
			#check that info contains a role

			if info['role'] == role:
				#if a signature is specified, then it has to be matched
				if (sign != '' and sign != info['signature']):
					logging.info("Found a {0} but it contains a wrong signaure".format(role))
					return None
				return {'path': path, 'info': info}

		except Exception as e:
			#print "No file in path", path, e
			return None;

	def getMaster(self, base_path,  filename='picloud.json'):
		"""
		Checks if the path passed as a parameter contains a master
		"""
		master = None
		for l in listdir(base_path) :
			path = base_path + "/" + l
			master = self.checkIs('master', path, '', filename)
			if master != None :
				return master

		return None

	def getSlave(self, base_path,  filename='picloud.json', sign=''):
		"""
		Checks if the path passed as a parameter contains a slave
		"""
		slave = None
		for l in listdir(base_path) :
			path = base_path + "/" + l
			slave = self.checkIs('slave', path, sign, filename)
			if slave != None:
				return slave;

		return None;

	def checkRunningProcessAndMark (self, filename):
		"""
		Check if another process is running, and if not, mark that this process
		is running the sync. 
		"""
		now = datetime.today()
		try:
			f = open(filename, "r")
		except Exception as e:
			#No other process is syncing
			f = open(filename, "w")
			syncMark = {'started': now.strftime(self.dateFormat)}
			print "printing syncMark"
			print syncMark
			json.dump(syncMark, f)
			#We can start syncing here
			return False
		
		logging.debug("Found a sync file")
		p = json.load(f)
		startedDate = datetime.strptime(p['started'], self.dateFormat)
		
		print startedDate
		dateDiff = now - startedDate
		if (dateDiff.days > 1):
			logging.error("Looks like a process has been running for {0} days, you might want to do something about it".format(dateDiff.days))
		if (dateDiff.days > 7):
			#Here we might want to send an email to the admin
			logging.error("Heyyyyy!!!! Something is really broken here. Please find out what's happening")
		return True


	def markSynced (self, path, filename, info):
		f = open(path + "/" + filename, 'w+')
		info['last_synced'] = datetime.today().strftime(self.dateFormat)
		json.dump(info, f)

	def run(self):
		"""
		Main method to run the script


		TODO: Try to run and see if it marks last_synced
		"""
		#check if master and slave are there
		info_file_name = self.CFG['INFO_FILE_NAME']
		base_dir = self.CFG['BASE_DIR']
		sync_file_name = self.CFG['SYNC_FILE_NAME']
		master = self.getMaster(base_dir, info_file_name)
		slave = None

		if master != None :
			logging.info("We have a master in {0}".format(master['path']))
			slave = self.getSlave(base_dir, info_file_name, master['info']['signature'])

		if slave != None:
			logging.info("We have a slave in {0}".format(slave['path']))

		if master!= None and slave != None:
			otherProcess = self.checkRunningProcessAndMark(sync_file_name)

			if otherProcess is False:
				#we can sync
				#TODO: what if the rsync command fails? 
				command = "rsync -avz --exclude={2} {0}/ {1}/"
				command = command.format(master['path'], slave['path'], info_file_name)
				logging.debug(command)
				resp = os.system(command)
				logging.debug(resp)
				self.markSynced(master['path'], info_file_name, master['info'])
				self.markSynced(slave['path'], info_file_name, slave['info'])
				resp = os.system("rm {0}".format(sync_file_name))

				#print command