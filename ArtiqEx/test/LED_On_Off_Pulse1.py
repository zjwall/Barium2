from artiq.experiment import *



class LED(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("led0")

    @kernel
    def run(self):
        self.core.reset()
        for i in range(10000):
            delay(1000*ms)
            self.led0.pulse(100*ms)


