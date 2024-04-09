from artiq.experiment import *



class zotino_test(EnvExperiment):
    def build(self):
        self.setattr_device("core")
        self.setattr_device("zotino0")

    @kernel
    def run(self):
        self.core.reset()                            
        self.zotino0.init()
        print(self.zotino0.read_reg(9))


