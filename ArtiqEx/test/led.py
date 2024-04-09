from artiq.experiment import *


class LED1(EnvExperiment):
    def build(self):
        print('hell')
        self.setattr_device("core")
        self.setattr_device("led0")

    @kernel
    def run(self):
        print('hi')
        self.core.reset()
        self.led0.on()
