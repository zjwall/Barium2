from artiq.experiment import *


class zotino_led(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def run(self):
    
        self.core.reset()                       #resets core device      
        self.core.break_realtime()              #moves timestamp forward to prevent underflow
                                                #this can also be achieved with a fixed delay    
        
        voltage = 5                  #defines voltage variable in Volts
        mu = self.zotino0.voltage_to_mu(voltage)
        self.zotino0.init()                     #initialises zotino0
        delay(200*us)                           #200us delay, needed to prevent underflow on initialisation
        
        self.zotino0.write_dac_mu(0,mu)       #writes voltage variable to DAC, channel 0
        self.zotino0.load()  
