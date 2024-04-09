from artiq.experiment import *
from artiq.master.databases import DeviceDB
from artiq.master.worker_db import DeviceManager



devices=DeviceDB('device_db.py')
dm=DeviceManager(devices)
core=dm.get('core')

class api(object):
    def __init__(self):
        self.core=core

    @kernel
    def on(self):
        core.reset()


api_obj=api()
api_obj.on()
