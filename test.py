import unittest
import json
from picloudsync import PiCloudSync
import os
from os import listdir

CFG = {}
CFG['BASE_DIR']='tests/data/discs'
CFG['INFO_FILE_NAME'] = 'picloud.json'
CFG['SYNC_FILE_NAME'] = 'pisync.json'

class PiCloudTest(unittest.TestCase):
	def getMasterSyncDate(self):
		f = open(self.cfg['BASE_DIR'] + '/master/' + self.cfg['INFO_FILE_NAME'])
		info = json.load(f)
		return info['last_synced']
	def commonSetUp(self): 
		self.sync = PiCloudSync(self.cfg)
		self.slaveDir = self.cfg['BASE_DIR'] + '/' + 'slave'
		self.masterDir = self.cfg['BASE_DIR'] + '/' + 'master'
		self.beforeSListDir = listdir(self.slaveDir)
		self.beforeMListDir = listdir(self.masterDir)
		self.beforeMSyncDate = self.getMasterSyncDate()


class TestsNoMaster(PiCloudTest):
	"""
	TC1
	Checks that if there's no master, nothing happens
	"""
	cfg = CFG.copy()
	def setUp(self):
		self.cfg['BASE_DIR'] = 'tests/data/discs_tc1'
		self.commonSetUp()
	
	def runTest(self):
		self.sync.run()
		newListDir = listdir(self.slaveDir)
		self.assertEqual(len(self.beforeSListDir), len(newListDir), 'The two dirs have different lengths'),
		self.assertEqual(self.beforeMSyncDate, self.getMasterSyncDate(), 'The sync date might have been updated on master')
		self.assertListEqual(newListDir, self.beforeSListDir, 'The two lists are different')

class TestsNoSlave(PiCloudTest):
	"""
	TC2
	Checks that if there's no slave, nothing happens
	"""
	cfg = CFG.copy()
	def setUp(self):
		self.cfg['BASE_DIR'] = 'tests/data/discs_tc2'
		self.commonSetUp()

	def runTest(self):
		self.sync.run()
		newListDir = listdir(self.slaveDir)
		self.assertEqual(len(self.beforeSListDir), len(newListDir), 'The two dirs have different lengths'),
		self.assertEqual(self.beforeMSyncDate, self.getMasterSyncDate(), 'The sync date might have been updated on master')
		self.assertListEqual(newListDir, self.beforeSListDir, 'The two lists are different')

class TestsGoodSync(PiCloudTest):
	"""
	TC3
	Checks that if there's both, master and slave they're synced
	"""
	cfg = CFG.copy()
	def setUp(self):
		self.cfg['BASE_DIR'] = 'tests/data/discs_tc3'
		command = 'rm -rf {0}'.format(self.cfg['BASE_DIR'] + '/slave/*.txt')
		print command
		os.system(command)
		self.commonSetUp()

	def runTest(self):
		self.sync.run()
		newListDir = listdir(self.slaveDir)

		self.assertEqual(len(newListDir), len(self.beforeMListDir), 'The two dirs have different lengths'),
		self.assertNotEqual(self.beforeMSyncDate, self.getMasterSyncDate(), 'The sync date might have been updated on master')
		self.assertListEqual(self.beforeMListDir, newListDir, 'The two lists are different')


def suite():
	t_suite = unittest.TestSuite()
	t_suite.addTest(unittest.makeSuite(TestsNoMaster))
	t_suite.addTest(unittest.makeSuite(TestsNoSlave))
	t_suite.addTest(unittest.makeSuite(TestsGoodSync))
	return t_suite

if __name__=='__main__':
	runner = unittest.TextTestRunner(verbosity=2)
	test_suite = suite()
	runner.run(test_suite)
