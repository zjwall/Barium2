import labrad
from twisted.internet.defer import inlineCallbacks, returnValue
from common.lib.servers.script_scanner.experiment import experiment

from labrad.units import WithUnit
import numpy as np
from config.multiplexerclient_config import multiplexer_config
import time
import socket
import os
import datetime as datetime


class flourescence_detection(experiment):

    name = 'Flourescence Detection'

    exp_parameters = [('FlourescenceDetection', 'Delay_Time'),
                      ('FlourescenceDetection', 'Collection_Time'),
                      ('FlourescenceDetection', 'Cycles'),
                      ('FlourescenceDetection', 'Num_Pts_to_Avg')]


    try:
        exp_parameters.extend(main_sequence.all_required_parameters())
    except:
        pass

    @classmethod
    def all_required_parameters(cls):
        return cls.exp_parameters


    def initialize(self, cxn, context, ident):

        self.ident = ident
        self.wm_p = multiplexer_config.info
        self.cxn = labrad.connect(name = 'Flourescence Detection')
        self.artiq = self.cxn.artiq_server

        self.grapher = self.cxn.real_simple_grapher
        self.dv = self.cxn.data_vault
        
        # Define variables to be used
        self.p = self.parameters
        self.repeat_num = self.p['FlourescenceDetection.Num_Pts_to_Avg']


        # Get contexts for saving the data sets
        self.c_pmt = self.cxn.context()
        self.set_up_datavault()
       

    def run(self, cxn, context):

        '''
        Main loop ------ the old pulser calls program pulse sequence with the pulse sequence file which
        then pull the required paraemters from parameter vault ---- we now retrieve the parameter vault paramaters in
        the experiment file and pass them as arguments to the artiq server and the artiq experiment sequence
        '''
        
        exp_num = 0

        keys = list(self.p.keys())[:-1]
        params = list(self.p.values())[:-1]
        for k in range(len(params)):
            params[k] = (float(params[k]))
        for i in range(int(self.repeat_num)):
            mean_pmt_count = 0.0
            self.artiq.program_pulse_sequence("flourescence.py", keys, params)
        
            try:
                pmt_counts = self.artiq.get_exp_counts()
            except:
                print('failed to get counts')
            mean_pmt_count = np.mean(pmt_counts)
            self.dv.add(exp_num, mean_pmt_count, context = self.c_pmt)
            exp_num += 1
        

    def set_up_datavault(self):
        # set up folder
        date = datetime.datetime.now()
        year  = str(date.year)
        month = '%02d' % date.month  # Padded with a zero if one digit
        day   = '%02d' % date.day    # Padded with a zero if one digit
        trunk = year + '_' + str(month) + '_' + str(day)

        # Open new data sets for prob and saving histogram data
        self.dv.cd(['',year,month,trunk],True, context = self.c_pmt)
        dataset = self.dv.new('Flourescence_Detection',[('freq', 'kHz')],[('Counts', 'Counts', 'num')], context = self.c_pmt)
        # add dv params
        for parameter in self.p:
            self.dv.add_parameter(parameter, self.p[parameter], context = self.c_pmt)


        # Set live plotting
        self.grapher.plot(dataset, 'bright/dark', False)





if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = flourescence_detection(cxn=cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
