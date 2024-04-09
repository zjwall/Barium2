from artiq.experiment import *


class Tutorial(EnvExperiment):

    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl15")
        
    @kernel
    def run(self):
        self.core.reset()
        for i in range(int(self.Pulse_Number)):
            delay(2*us)
            self.ttl15.pulse(2*us)
        


    def get_readout_counts(self):
        return(self.counts)
    
    def set_vals(self, keys, vals):
        self.p = dict(zip(keys, vals))
        self.Pulse_Number = self.p['TestSequence.Pulse_Number']





