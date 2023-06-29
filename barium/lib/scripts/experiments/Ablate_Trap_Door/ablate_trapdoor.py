import labrad
from twisted.internet.defer import inlineCallbacks, returnValue
#from common.lib.servers.abstractservers.script_scanner.scan_methods import experiment
from labrad.units import WithUnit
from barium.lib.scripts.pulse_sequences.AblateTrapdoor import ablate_trapdoor as main_sequence
import numpy as np
from config.multiplexerclient_config import multiplexer_config
import time
import socket
import os
import datetime as datetime


class ablate_trapdoor(experiment):

    name = 'Ablate Trapdoor'

    exp_parameters = []
    
    @classmethod
    def all_required_parameters(cls):
        return cls.exp_parameters


    def initialize(self, cxn, context, ident):

        self.ident = ident
        self.wm_p = multiplexer_config.info
        self.cxn = labrad.connect(name = 'Ablate Trapdoor')
        self.cxnwlm = labrad.connect(multiplexer_config.ip, name = 'Ablate Trapdoor', password = 'lab')


        # Define variables to be used
        self.p = self.parameters
       

    def run(self, cxn, context):

        '''
        Main loop
        '''

        # program sequence to be repeated
        pulse_sequence = main_sequence(self.p)
        pulse_sequence.programSequence(self.pulser)

    def finalize(self, cxn, context):
        self.cxnwlm.disconnect()


if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = ablate_trapdoor(cxn=cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
