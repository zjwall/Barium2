from artiq.experiment import *
from artiq_api import ARTIQ_api

class zotino_led(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def run(self):
    
        self.core.reset()                       #resets core device      
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can also be achieved with a fixed delay    
        
        voltage = 2                  #defines voltage variable in Volts
        
        self.zotino0.init()                     #initialises zotino0
        delay(200*us)                           #200us delay, needed to prevent underflow on initialisation
        
        self.zotino0.write_dac(9,voltage)       #writes voltage variable to DAC, channel 0
        self.zotino0.load()  


ddb_filepath = "device_db.py"
devices = DeviceDB(ddb_filepath)
device_manager = DeviceManager(devices)
device_db = devices.get_device_db()


core = device_manager.get("core")

x = zotino_led(ARTIQ_api(ddb_filepath))


##__server__ = AgilentServer()
##
##if __name__ == '__main__':
##    from labrad import util
##    util.runServer(__server__)
