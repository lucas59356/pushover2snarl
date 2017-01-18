#! /bin/env python3
import requests
from cfg import config

def login(user_login = config['pushover']['login'], user_passwd = config['pushover']['passwd'], user_key = config['pushover']['key'], pushover_base = config['pushover']['base_url']):
    """
        Make the user login in pushover API
    """
    data = {
        "email": user_login,
        "password": user_passwd
    }
    r = requests.post(pushover_base+'/1/users/login.json', data=data)
    if r.ok:
        return r.json()
    else:
        r.raise_for_status()
        print(r.text)
