
from artiq.experiment import *
from artiq.coredevice.core import Core
from artiq.coredevice.urukul import CPLD as UrukulCPLD
from artiq.coredevice.ad9910 import AD9910


class urukulOFF(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")
        self.setattr_device("urukul0_ch0")
        self.setattr_device("urukul0_ch1")
    @kernel
    def run(self):
        self.core.reset()
        while not self.core.get_rtio_destination_status(0):
            pass
        
        while not self.core.get_rtio_destination_status(1):
            pass
        self.core.break_realtime()
        self.urukul0_cpld.init()
        delay(.1 * ms)
        self.urukul0_ch0.init() #initialise and configure the DDS channel
        self.urukul0_ch1.init() #initialise and configure the DDS channel
        delay(.1 * ms)
        #CH0
        #CH1
        self.urukul0_ch0.sw.off() #turn on the DDS ouput
        self.urukul0_ch1.sw.off() #turn on the DDS ouput
