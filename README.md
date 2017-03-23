#Pushover2snarl

# PFAQ - Possible Frequent Asked Questions

- What this software do?

It consumes the pushover api and notify the last message (if diferent that before) using snarl api.

- What i need to run this?

A pushover account (course), python 3.x (I write and test in 3.6) and the requests package (installable by typing pip install -r requirements.txt) and something to make it do something, like an IFTTT integration and some applets.

- Good, what script I need to run?

The script is main.py, just run this and snarl and the engine start to work

- I see a curl output, WTF!

This is a little workaround to dribble the urlencode function on requests. The message in snarl without this is showed all urlencoded and stackoverflow not resolved my problem in this case.

- I need to config something?

Course, all the configs are in the config.json and deviceid.txt, just copy the templates to the original names and put the infos.

# TODO
- Make it better :p
