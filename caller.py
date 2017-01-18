import queue
import listener
import requests
import sys
import time
from cfg import config

global q
q = queue.Queue()

def caller():
    """
        Call other functions and fetch the data from pushover API
    """
    data = listener.listen()
    lmsg = {}
    try:
        msg = requests.get(config['pushover']['base_url'] + "/1/messages.json", data).json()['messages'][-1]
    except KeyError:
        msg = {"error": "Noting yet"}

    while 1:
        if not lmsg == msg:
            msg = requests.get(config['pushover']['base_url'] + "/1/messages.json", data)
            if msg.ok:
                msg = msg.json()['messages'][-1]
                q.put_nowait(msg)
            else:
                msg.raise_for_status()
                msg.text
        time.sleep(10)
print("Your client ID: " + listener.me['id'])

