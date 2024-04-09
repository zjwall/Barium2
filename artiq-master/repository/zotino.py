from artiq.experiment import *

class zotino_led(EnvExperiment):
    def build(self):
        for i in range(16):
            self.setattr_argument("voltage"+str(i), NumberValue(ndecimals=3, step=.01))
        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def run(self):
        vol = [self.voltage0,self.voltage1,self.voltage2,self.voltage3,self.voltage4,self.voltage5,self.voltage6,self.voltage7, self.voltage8,self.voltage9,self.voltage10,self.voltage11,self.voltage12,self.voltage13,self.voltage14,self.voltage15]
        self.core.reset()                            
        self.zotino0.init()                    
        delay(200*us)
        for i in range(16):
            self.zotino0.write_dac(i,vol[i])
            delay(200*us)
        self.zotino0.load()  


