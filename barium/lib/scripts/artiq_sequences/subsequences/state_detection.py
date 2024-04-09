from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time
import numpy as np

class StateDetection(HasEnvironment):

    def build(self):
        self.setattr_device("PMT")
        self.setattr_device("PMT_counter")
        
    @kernel(flags={"fast-math"})
    def run(self, dur):
        self.PMT_counter.gate_rising(dur*us)

    def set_params(self, dur):
        self.dc_duration = dur


    @kernel(flags={"fast-math"})
    def fetch_count(self) -> TInt32:
        """
        Convenience function so that users don't have to separately instantiate the PMT
        device object to read counts.
        """
        return self.PMT_counter.fetch_count()
