from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time

import numpy as np

class PhotonCounterCurrent2(EnvExperiment): 
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl0")
        self.setattr_device("ttl0_counter")
        self.setattr_device("ttl1")
        self.setattr_device("ttl2")

        self.setattr_device("ttl3")
        self.setattr_device("ttl3_counter")

        self.setattr_argument("n_points", NumberValue(1000,ndecimals=0, step=1))  #steps number
        self.setattr_argument("det_time", NumberValue(0.01*ms,ndecimals=3, unit="ms", step=0.001))  #time of detection
        self._num_counts_tmp = 0
        

    def run(self):
        tc = time.time()     
        try:
            self.run_kernel()
        except TerminationRequested:
            print('Terminated.') 
            
        print("Time elapsed: {:.2f} seconds" .format(time.time() - tc))        
            

    @kernel
    def run_tmp(self):

                                 
        i = 0 ;

        self.set_dataset("Photon_Counts", np.full(self.n_points, np.nan), broadcast=True)
        
        self.core.break_realtime()
        
        delay(10*ms)
        

        for _ in range(self.n_points):        
            num_rising_edges = self.counting_style4()
            delay(100*us)
            self.mutate_dataset("Photon_Counts", i, num_rising_edges)
            i += 1
            self._num_counts_tmp = num_rising_edges

        print(self._num_counts_tmp)


    @kernel
    def run(self):
        self.core.reset()
        self.core.break_realtime()
        self.ttl0.input()
        self.core.break_realtime()
        self.ttl1.input()
        self.core.break_realtime()
        self.ttl2.input()
        self.core.break_realtime()
        self.ttl3.input()
        self.core.break_realtime()
        self.ttl0_counter.gate_rising_mu(1000000)
        self._num_counts_tmp = self.ttl0_counter.fetch_count()
        self.core.break_realtime()
        self.core.break_realtime()
        print(self._num_counts_tmp)
        self.core.break_realtime()
            

    @kernel
    def counting_style4(self):        
        self.ttl0_counter.gate_rising(self.det_time) #needs to be initialised in the programme
        
        return self.ttl0_counter.fetch_count()
    
    @kernel
    def counting_style3(self):
        gate_end_mu = self.ttl0.gate_rising(self.det_time)
     
        return self.ttl0.count(now_mu())
