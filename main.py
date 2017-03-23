import json
import requests
import time
import os

cfg = json.load(open("config.json"))

BASE_URL = cfg['pushover']['base_url']

def request_to_api(path, data):
    """
        Request something to the pushover api
    """
    return requests.post(BASE_URL + path, data = data).json()

def get_to_api(path, data):
    """
        Request something to the pushover api
    """
    return requests.get(BASE_URL + path, data = data).json()

def pushover_get_device(name="cmd", l_os='O'):
    """
        Get and configure the device id used by me
    """
    data = {
        "secret": secret,
        "name": name,
        "os": l_os
    }
    dapi = requests.post(BASE_URL + '/1/devices.json', data)
    if not dapi.ok:
        print("Algum problema ocorreu ao fazer requisição do id de cliente")
        print("Tentando ler do arquivo")
        d = open('deviceid.txt').read()
    else:
        d = dapi.json()['id']
        f = open('deviceid.txt','w')
        f.write(d)
        f.close()

    print("Device id: %s" %d)
    return d

def pushover_login():
    """
        Get the secret to login in the api using the login credentials
    """
    data = {
        "email": cfg['pushover']['login'],
        "password": cfg['pushover']['passwd']
    }
    return request_to_api('/1/users/login.json', data)['secret']

def pushover_get_messages():
    """
        Fetch the messages from the API
    """
    data = {
        "device_id": device_id,
        "secret": secret
    }
    return get_to_api('/1/messages.json', data)['messages']

def snarl_request(method, data):
    """
        Request something to a SNP server
    """
    return requests.get(cfg['snarl']['url'] %method, data)

def snarl_register():
    """
        Register a app on SNP server
    """
    data = {
        "app-sig": cfg['snarl']['app_sig'],
        "uid": 1,
        "title": cfg['snarl']['default_title'],
        "keep-alive": True
    }
    r = snarl_request("register", data)
    if not r.ok:
        r.raise_for_status()
    return r

def snarl_hello():
    """
        Send a hello request to a SNP server
    """
    data = {
        "app-sig": cfg['snarl']['app_sig']
    }
    return snarl_request('hello', data)

def snarl_addclass(msg):
    """
        Receives a json from pushover parse and add a class based on it
    """
    data = {
        "app-sig": cfg['snarl']['app_sig'],
        "name": msg['app'],
        "title": msg['app'],
        "icon": cfg['snarl']['default_icon'],
        "id": msg['aid']
    }
    r = snarl_request('addclass', data)
    if not r.ok:
        r.raise_for_status()
    return r

def snarl_notify(msg):
    """
        Send a snarl/SNP notification
        I use curl to this not urlencode the text
    """
    if not "title" in msg:
        msg['title'] = msg['app']
    data = "?app-sig=%s&timeout=%s&uid=%s&id=%s&title=%s&text=%s" %(cfg['snarl']['app_sig'], str(10), str(msg['id']), str(msg['aid']),str(msg['title']) ,str(msg['message']))
    method = 'notify'
    url = cfg['snarl']['url'] %method
    os.system(""" curl "%s%s"  """ %(url, data))

secret = pushover_login()
device_id = pushover_get_device()
snarl_register()
snarl_hello()

last_message = 0
while 1:
    msgs = pushover_get_messages()
    for m in msgs:
        if m['id'] > last_message:
            snarl_notify(m)
            last_message = m['id']
    time.sleep(2)