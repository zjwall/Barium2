from artiq.experiment import *


def print_underflow():
    print("RTIO underflow occured")

class Tutorial(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("ttl8")

    @kernel
    def run(self):
        self.core.reset()
        try:
            for i in range(10000):
                self.ttl8.pulse(1000*ns)
                delay(1000*ns)
        except RTIOUnderflow:
            print_underflow()
