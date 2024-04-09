from artiq.experiment import *

class th1(EnvExperiment):
    """
    tmp
    """

    
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul1_cpld")
        self.setattr_device("urukul0_cpld")
        self.setattr_device("urukul2_cpld")
        self.setattr_device("urukul2_ch0")
        self.setattr_device("urukul2_ch1")
        self.setattr_device("urukul2_ch2")
    
        

    @kernel
    def run(self):
        self.core.reset()
        #self.urukul2_cpld.init()
        #self.core.break_realtime()
        #self.urukul2_ch0.init()
        #self.core.break_realtime()
        #self.urukul2_ch1.init()

        #self.core.break_realtime()
        #self.urukul2_ch1.cfg_sw(1)
        self.urukul2_ch0.cfg_sw(1)
        


