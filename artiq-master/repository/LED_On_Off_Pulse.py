from artiq.experiment import *


class LED2(EnvExperiment):
    def build(self):
        self.setattr_argument("count", NumberValue(ndecimals=0, step=1))
        self.setattr_device("core")
        self.setattr_device("led0")

    @kernel
    def run(self):
        print('hi')
        self.core.reset()
        for i in range(self.count):
            delay(100*ms)
            self.led0.pulse(100*ms)                    #led turns on for 5s then turns off
        print('done')
