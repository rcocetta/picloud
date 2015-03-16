# picloud
Personal backup system for Raspberry pi

## What is this thing? 
This is a little program that allows you to keep 2 discs in sync in a master slave configuration, so that you can take the master with you and always keep a safe copy on the slave connected to your Pi.

My initial thoughts are detailed [here](https://github.com/rcocetta/picloud/wiki/First-Thoughts)

## Use 
### Run the system as it is
```
python main.py run 
```
### Install it in crontab
Make it run every minute

```
python main.py install
```

**While writing it, I realised that, of course it'll work on any Linux machine with Python installed.**