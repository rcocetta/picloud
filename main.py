import json
from settings import *
import logging
from os import listdir
from datetime import datetime
from datetime import date

LOG_FORMAT = "%(asctime)-15s - [PiCloudMain][%(levelname)s] - %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=logging.DEBUG)
logging.getLogger("picloud")

def checkIs(role, path, sign='', filename='picloud.json'):
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

def getMaster(base_path,  filename='picloud.json'):
	"""
	Checks if the path passed as a parameter contains a master
	"""
	master = None
	for l in listdir(base_path) :
		path = BASE_DIR + "/" + l
		master = checkIs('master', path, '', filename)
		if master != None :
			return master

	return None

def getSlave(base_path,  filename='picloud.json', sign=''):
	"""
	Checks if the path passed as a parameter contains a slave
	"""
	slave = None
	for l in listdir(base_path) :
		path = BASE_DIR + "/" + l
		slave = checkIs('slave', path, sign, filename)
		if slave != None:
			return slave;

	return None;

def handleSyncStart (filename):
	now = datetime.today()
	dateFormat = "%Y-%m-%d %H:%M:%S"
	try:
		f = open(filename, "r")
	except Exception as e:
		#No other process is syncing
		f = open(filename, "w")
		syncMark = {'started': now.strftime(dateFormat)}
		print "printing syncMark"
		print syncMark
		json.dump(syncMark, f)
		#We can start syncing here
		return None
	
	logging.debug("Found a sync file")
	p = json.load(f)
	startedDate = datetime.strptime(p['started'], dateFormat)
	
	print startedDate
	dateDiff = now - startedDate
	if (dateDiff.days > 1):
		logging.error("Looks like a process has been running for {0} days, you might want to do something about it".format(dateDiff.days))
	if (dateDiff.days > 7):
		#Here we might want to send an email to the admin
		logging.error("Heyyyyy!!!! Something is really broken here. Please find out what's happening")



def run():
	#check if master and slave are there
	master = getMaster(BASE_DIR, INFO_FILE_NAME)
	slave = None

	if master != None :
		logging.info("We have a master in {0}".format(master['path']))
		slave = getSlave(BASE_DIR, INFO_FILE_NAME, master['info']['signature'])

	if slave != None:
		logging.info("We have a slave in {0}".format(slave['path']))

	if master!= None and slave != None:
		handleSyncStart("pisync.json")

run()