from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time

import numpy as np

class PhotonCounterCurrent2(EnvExperiment): 
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl2")
        self.setattr_device("ttl2_counter")
        self.n_points = 10
        self.det_time = .01*ms


    def run(self):
        tc = time.time()     
        try:
            self.run_kernel()
        except TerminationRequested:
            print('Terminated.') 
            
        print("Time elapsed: {:.2f} seconds" .format(time.time() - tc))        
            

    @kernel
    def run_kernel(self):

        self.core.reset()
                                 
        i = 0 ;

        self.set_dataset("Photon_Counts", np.full(self.n_points, np.nan), broadcast=True)
        
        # self.core.break_realtime()
        delay(10*ms)
        

        for _ in range(self.n_points):        
            num_rising_edges = self.counting_style3()
            delay(100*us)
            self.mutate_dataset("Photon_Counts", i, num_rising_edges)
            delay(100*ms)
            print(num_rising_edges)
            i += 1


    @kernel
    def counting_style4(self):        
        self.ttl2_counter.gate_rising(self.det_time) #needs to be initialised in the programme
        
        return self.ttl2_counter.fetch_count()
    
    @kernel
    def counting_style3(self):
        gate_end_mu = self.ttl2.gate_rising(self.det_time)
     
        return self.ttl2.count(now_mu())
