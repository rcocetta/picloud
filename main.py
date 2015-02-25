import json
from settings import *
from os import listdir

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
		print 'info here is {0}, {1}'.format(role, info['role'])

		if info['role'] == role:
			print 'Hey'
			#if a signature is specified, then it has to be matched
			if (sign != '' and sign != info['signature']):
				print "wrong sign"
				return None
			print "Found a " + role + " in " + path
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



master = getMaster(BASE_DIR, INFO_FILE_NAME)
slave = None

if master != None :
	print "We have a master {0}".format(master)
	slave = getSlave(BASE_DIR, INFO_FILE_NAME, master['info']['signature'])

print "We have a slave {0}".format(slave)