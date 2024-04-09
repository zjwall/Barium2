from artiq.experiment import *


class Tutorial(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl8")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl8.output()
        for i in range(1000000):
            delay(2*us)
            self.ttl8.pulse(2*us)
