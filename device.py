#! /bin/env python3
from cfg import config
import requests
import login

def regDevice (name="cmd", os="O", pushover_base=config['pushover']['base_url']):
    """
        Register a pushover device
        Based on tutorial: https://pushover.net/api/client
    """
    data = {
        "secret": login.login()['secret'],
        "name": name,
        "os": os
    }
    dev = open('deviceid.txt','r')
    dev_raw = dev.read()
    if dev_raw == '':
        r = requests.post(pushover_base + "/1/devices.json", data=data)
        if r.ok:
            return r.json()
            print(r.json()['id'])
        else:
            r.raise_for_status()
            print(r.text)
    else:
        return {"id": dev_raw}
        print(dev_raw)
