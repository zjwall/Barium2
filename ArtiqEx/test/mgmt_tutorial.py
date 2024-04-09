from artiq.experiment import *
import numpy as np
import time

class MgmtTutorial(EnvExperiment):
    """Management tutorial"""
    def build(self):
        self.count = 20
    def run(self):
        self.set_dataset("parabola", np.full(self.count, np.nan), broadcast=True)
        for i in range(self.count):
            self.mutate_dataset("parabola", i, i*i)
            time.sleep(0.5)
    
