import caller
import threading
import requests
import time
import telnetlib
import os
from cfg import config

t = threading.Thread(target=caller.caller)
t.start()

app_sig = config['snarl']['app_sig']

def register():
    data = {
        "app-sig": config['snarl']['app_sig'],
        "uid": 1,
        "title": config['snarl']['default_title'],
        "keep-alive": True
    }
    method = "register"
    r = requests.get(config['snarl']['url'] %method, data)
    if not r.ok:
        r.raise_for_status()

def hello():
    data = {
        "app-sig": app_sig
    }
    method = "hello"
    r = requests.get(config['snarl']['url'] %method, data)
    if not r.ok:
        r.raise_for_status()

def addclass(json):
    data = {
        "app-sig": app_sig,
        "name": json['app'],
        "title": json['app'],
        "icon": config['snarl']['default_icon'],
        "id": json['aid']
    }
    method = "addclass"
    r = requests.get(config['snarl']['url'] %method, data)
    if not r.ok:
        r.raise_for_status()

def notify(json):
    try:
        title = json['title']
    except KeyError:
        title = json['app']
    data = "?app-sig=%s&timeout=%s&uid=%s&id=%s&title=%s&text=%s" %(app_sig, str(10), str(json['id']), str(json['aid']),str(title) ,str(json['message']))
    method = "notify"
    url = config['snarl']['url'] %method
    os.popen("""curl "%s%s" """ %(url, data)) # Só assim pra dar certo :v pelo requests ele fica encodando url sozinho.

register()
hello()
q = caller.q
ov = {}
while 1:
    v = q.get()
    if not v==ov:
        addclass(v)
        notify(v)
    ov = v.copy()
    q.task_done()
    time.sleep(1)
