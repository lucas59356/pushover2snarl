import websocket
import device
import login
import json

me = device.regDevice()
auth = login.login()

def listen(callback=print):
    devID = me['id']
    meSecret = auth['secret']
    return {
        "device_id": devID,
        "secret": meSecret
    }
