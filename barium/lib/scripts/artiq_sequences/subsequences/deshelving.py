from artiq.experiment import *
from artiq.coredevice.edge_counter import CounterOverflow
import time
import numpy as np

class Deshelving(HasEnvironment):

    def build(self):
        self.setattr_device("deshelving_AOM")

        
    @kernel(flags={"fast-math"})
    def run(self, dur):
        self.deshelving_AOM.sw.on()
        delay(dur*us)

