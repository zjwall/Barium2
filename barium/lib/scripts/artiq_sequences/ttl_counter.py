from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time

import numpy as np

class PhotonCounterCurrent2(EnvExperiment): 
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl0_counter")
        self.n_points = 10
        self.det_time = .01*ms
        self.counts = [0] * self.n_points
      
            

    @kernel
    def run(self):

        self.core.reset()
                                 
        i = 0 ;

        self.set_dataset("Photon_Counts", np.full(self.n_points, np.nan), broadcast=True)
        
        # self.core.break_realtime()
        delay(10*ms)
        

        for i in range(self.n_points):
            self.core.break_realtime()
            self.ttl0_counter.gate_rising(self.det_time)
            x = self.ttl0_counter.fetch_count()
            self.counts[i] = x

    
    @kernel
    def counting_style3(self):
        gate_end_mu = self.ttl0.gate_rising(self.det_time)
     
        return self.ttl0.count(now_mu())


    @rpc(flags={"async"})
    def _recordTTLCounts(self, value, index):
        """
        Records values via rpc to minimize kernel overhead.
        """
        self.ttl_counts_array[index] = value

        
    def get_counts(self):
        return(self.counts)

    def set_vals(self, keys, vals):
        self.p = dict(zip(keys, vals))
        self.Pulse_Number = self.p['TestSequence.Pulse_Number']
