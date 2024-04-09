
from artiq.experiment import *
from artiq.coredevice.core import Core
from artiq.coredevice.urukul import CPLD as UrukulCPLD
from artiq.coredevice.ad9910 import AD9910


class urukul(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        #self.setattr_device("urukul0_cpld")
        self.setattr_device("urukul0_ch0")


        
    @kernel
    def run(self):
        self.core.reset()
##        self.urukul2_cpld.init()
##        self.urukul2_ch0.init()
##        self.urukul2_ch0.set(50*MHz,0.01)
        self.urukul0_ch0.sw.on()

##        self.urukul0_cpld.init()
##        self.urukul0_ch0.init()
        delay(.1*s)
##        self.urukul0_ch0.set(50*MHz,0.01)
##        self.urukul0_ch0.sw.on()
##       self.urukul0_cpld.set_att(0,20.0)
##        print(self.urukul0_cpld.get_channel_att(0))
        
        #self.urukul0_ch0.set(50*MHz,amplitude = .5) #sets freq in MHz, amplitude and phase
        #self.urukul0_ch1.set(50*MHz,amplitude = .1) #sets freq in MHz, amplitude and phase

        
##        self.core.reset()
##        while not self.core.get_rtio_destination_status(0):
##            pass
##        
##        while not self.core.get_rtio_destination_status(1):
##            pass
##        self.core.break_realtime()
##        self.urukul0_cpld.init()
##        delay(.1 * ms)
##        self.urukul0_ch0.init() #initialise and configure the DDS channel
####        self.urukul0_ch1.init() #initialise and configure the DDS channel
##        delay(.1 * ms)
##        FREQ0_MHZ = 10*MHz
##        FREQ1_MHZ = 200*MHz
##        FREQ2_MHZ = 160*MHz
##        #CH0
##        self.urukul0_ch0.set_frequency(FREQ0_MHZ) #sets freq in MHz, amplitude and phase
##        self.urukul0_ch0.sw.on() #turn on the DDS ouput
##        #CH1
##        self.urukul0_ch1.set_att(10.0) #set digital step attenuator in SI units
####        self.urukul0_ch1.set(FREQ_MHZ1,1.0,1.0) #sets freq in MHz, amplitude and phase
####        self.urukul0_ch1.sw.on() #turn on the DDS ouput
##        #self.urukul0_ch0.sw.off() #turn on the DDS ouput



