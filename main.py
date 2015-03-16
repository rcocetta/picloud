from picloudsync import PiCloudSync
from settings import CFG
import argparse
import os


parser = argparse.ArgumentParser()
parser.add_argument("-r", "--run", help="Runs pisync once", action="store_true")
parser.add_argument("-i", "--install", help="Installs pisync in the cronjobs, ran from the directory you're running this command from", action="store_true")

args = parser.parse_args()

if args.install:
	print "Running in install mode"
	os.system("crontab -l > cronjob")
	os.system('echo "* * * * * cd $PWD; ptyhon main.py run; cd -" >> cronjob')
	os.system('crontab cronjob')

elif args.run: 
	print "Running in run mode"
	sync = PiCloudSync(CFG)
	sync.run()