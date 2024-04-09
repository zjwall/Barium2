from artiq.experiment import *


class Tutorial(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl8")
        self.setattr_device("ttl9")

    @kernel
    def run(self):
        self.core.reset()
        self.ttl8.output()
        self.ttl9.output()
        for i in range(100000):
            with parallel:
                self.ttl8.pulse(2*us)
                self.ttl9.pulse(2*us)
            delay(4*us)
