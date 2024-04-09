from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time

import numpy as np
import barium.lib.scripts.artiq_sequences.subsequences.doppler_cooling_2 as doppler_cooling
import barium.lib.scripts.artiq_sequences.subsequences.shelving_sub as shelving_sub
import barium.lib.scripts.artiq_sequences.subsequences.state_detection as state_detection
import barium.lib.scripts.artiq_sequences.subsequences.deshelving as deshelving



class Shelving(EnvExperiment): 
    def build(self):
        self.setattr_device("core")
        self.setattr_device("repump_AOM")
        self.dc = doppler_cooling.DopplerCooling(self)
        self.ss = shelving_sub.Shelving(self)
        self.sd = state_detection.StateDetection(self)
        self.ds = deshelving.Deshelving(self)
        self.dc_counts = []
        self.sd_counts = []
        self.col_time = 100
        
            
    @kernel(flags={"fast-math"})
    def run(self):

        self.core.reset()
                                 
        i = 0 ;

        delay(10*ms)

        for i in range(self.cycles):
            y=0
            x=0
            self.core.break_realtime()
            self.dc.run(self.dc_time)
            self.ss.run(self.shelve_time)
            
            self.sd.run(self.sd_time)
            self.ds.run(self.deshelve_time)
            x = self.dc.fetch_count()
            delay(1*ms)
            y = self.sd.fetch_count()

            self.dc_counts[i] = x
            self.sd_counts[i] = y


        
    def get_counts(self):
        self.total_counts[0] = self.dc_counts
        self.total_counts[1] = self.sd_counts
        return self.total_counts

    def set_vals(self, keys, vals):
        self.p = dict(zip(keys, vals))
        self.cycles = int(self.p['Shelving.cycles'])
        self.dc_time = float(self.p['DopplerCooling.duration'])
        self.shelve_time = float(self.p['time'])
        self.sd_time = float(self.p['StateDetection.duration'])
        self.deshelve_time = float(self.p['Deshelving.duration'])
        self.dc_counts = [0]*self.cycles
        self.sd_counts = [0]*self.cycles
        self.total_counts = [[0]*self.cycles]*2


