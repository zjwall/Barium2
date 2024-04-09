from artiq.experiment import *
from barium.lib.scripts.pulse_sequences.test_sequence import test_sequence as main_sequence


class Tutorial(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl15")
        
    @kernel
    def run(self):
        self.core.reset()
        self.ttl15.output()
        for i in range(100000):
            delay(2*us)
            self.ttl15.pulse(2*us)


    def get_readout_counts(self):
        return(self.counts)
    
    def set_vals(self, keys, vals):
        self.params = vals
        
