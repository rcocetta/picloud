# PiCloud

A project to build your safe disk storage solution with RaspberryPi. ... well and make it accessible to people in your network. 

## What does the software in this repo do? 

### The python script

Plugging 2 external storage devices in your Raspberry Pi it makes sure data is copied from one to the other, independently from when you plug your device, or if you take it with you. 

## What else do I need to have a "cloud" solution? 

Well, I'll install a Filezilla FTP server so that it'll be possilbe to reach your data from other computers in the same network.


##Motivation
I've recently been wondering:
   * What could be the type of storage I want for my personal data ?
   * How can I make sure I'm not going to lose all my pics, or all my movies ?
   * How can I safely store my data not using a 3rd party system ?

Well, the answer is: 2 Hard Disks, a Raspberry Pi, and this software

## How does it work? 

The crontab launches a script every hour that checks 2 things: 

    * The master disk is mounted 
    * No other backup process is running

If the 2 conditions are true, it starts an 

'''
rsync [master on slave]
''' 

If they're false for 1 day, it logs the failure, if they're false for many days, it sends an email to the admin.

### Recognise the master/slave
   * The script recognises the master and slave disks by a signature JSON file that contains.
      * role (master or slave)
      * lastSyncStarted
      * lastSyncEnded
   * The master slave configuration has to be independent from the mountpoint

### IPC communication
   The process run needs to check the presence of another process there. How? ... we'll find out.


## Possible Improvements

  * The signature can be unique so that once 2 disks are marked as master/slave they'll only be master and slave of each other.