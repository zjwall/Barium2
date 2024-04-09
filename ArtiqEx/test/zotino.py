from artiq.experiment import *

class zotino_led(EnvExperiment):
    def build(self):
        for i in range(16):
            self.setattr_argument("voltage"+str(i), NumberValue(ndecimals=0, step=1))
        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def run(self):
        self.core.reset()                            
        self.zotino0.init()                    
        delay(200*us)
        for i in range(16):
            self.zotino0.write_dac(i,self.voltage0)
            delay(200*us)
        self.zotino0.load()  


