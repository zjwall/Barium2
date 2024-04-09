from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time

import numpy as np

class PhotonCounterCurrent2(EnvExperiment): 
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl0_counter")
        self.setattr_device("ttl11")
        self.counts = []
      
            

    @kernel
    def run(self):

        self.core.reset()
                                 
        i = 0 ;

        
        # self.core.break_realtime()
        delay(10*ms)
        

        for i in range(self.cycles):
            self.core.break_realtime()
            with parallel:
                self.ttl11.pulse(3*us)
                with sequential:
                    delay(self.delay_time*us)                      
                    self.ttl0_counter.gate_rising(self.col_time*us)
                    x = self.ttl0_counter.fetch_count()
            self.counts[i] = x



        
    def get_counts(self):
        return(self.counts)

    def set_vals(self, keys, vals):
        self.p = dict(zip(keys, vals))
        self.cycles = int(self.p['FlourescenceDetection.Cycles'])
        self.delay_time = self.p['FlourescenceDetection.Delay_Time']
        self.col_time = self.p['FlourescenceDetection.Collection_Time']
        self.counts = [0]*self.cycles
