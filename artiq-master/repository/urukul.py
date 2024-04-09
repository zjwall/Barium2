
from artiq.experiment import *
#from artiq.coredevice.core import Core
#from artiq.coredevice.urukul import CPLD as UrukulCPLD
#from artiq.coredevice.ad9910 import AD9910


class urukul(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("urukul0_cpld")
        self.setattr_device("urukul0_ch0")
        self.setattr_device("urukul1_cpld")
        self.setattr_device("urukul1_ch0")
        self.setattr_device("urukul2_cpld")
        self.setattr_device("urukul2_ch0")
        
    def prepare(self):
        print('thkim')
        
    @kernel
    def run(self):
        self.core.reset()
        self.urukul1_cpld.init()
        self.core.break_realtime()
##        self.core.break_realtime()
##        delay(.1 * ms)
##        self.urukul0_ch0.init() 
##        delay(.1 * ms)
##        FREQ0_MHZ = 125*MHz
##        FREQ1_MHZ = 200*MHz
##        FREQ2_MHZ = 160*MHz
##        self.urukul0_ch0.set_frequency(FREQ0_MHZ) #sets freq in MHz, amplitude and phase
##        self.urukul0_ch0.sw.on() #turn on the DDS ouput
##        delay(2 * s)
##        self.urukul0_ch0.sw.off() #turn on the DDS ouput
##
        #FREQ0_MHZ = 125*MHz
        #FREQ1_MHZ = 200*MHz
        #FREQ2_MHZ = 160*MHz        
##        self.core.break_realtime()
##        self.urukul1_cpld.init()
##        delay(.1 * ms)
##        self.urukul1_ch0.init() 
##        delay(.1 * ms)
##        self.urukul1_ch0.set_frequency(FREQ0_MHZ) #sets freq in MHz, amplitude and phase
##        self.urukul1_ch0.sw.on() #turn on the DDS ouput
##        delay(10 * s)
##        self.urukul1_ch0.sw.off() #turn on the DDS ouput
##
        #self.core.break_realtime()
        #self.urukul2_cpld.init()
        #delay(.1 * ms)
        #self.urukul2_ch0.init() 
        #delay(.1 * ms)

        #self.urukul2_ch0.set_frequency(FREQ0_MHZ) #sets freq in MHz, amplitude and phase
        #self.urukul2_ch0.sw.on() #turn on the DDS ouput
        #delay(10 * s)
        #self.urukul2_ch0.sw.off() #turn on the DDS ouput

