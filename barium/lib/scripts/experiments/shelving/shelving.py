import labrad
from twisted.internet.defer import inlineCallbacks, returnValue
from common.lib.servers.script_scanner.experiment import experiment
from barium.lib.scripts.artiq_sequences.sequence_parameters.ShelvingSub import ShelvingSub as main_sequence

from labrad.units import WithUnit
import numpy as np
from config.multiplexerclient_config import multiplexer_config
import time
import socket
import os
import datetime as datetime


class shelving(experiment):

    name = 'Shelving'

    exp_parameters = [('Shelving', 'cycles'),
                      ('Shelving', 'Start_Time'),
                      ('Shelving', 'Stop_Time'),
                      ('Shelving', 'Time_Step'),
                      ('Shelving', 'dc_threshold'),
                      ]


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
        self.cxn = labrad.connect(name = 'Shelving')
        self.artiq = self.cxn.artiq_server

        self.grapher = self.cxn.real_simple_grapher
        self.dv = self.cxn.data_vault
        
        # Define variables to be used
        self.p = self.parameters
        self.cycles = self.p['Shelving.cycles']
        self.start_time = self.p['Shelving.Start_Time']
        self.stop_time = self.p['Shelving.Stop_Time']
        self.step_time = self.p['Shelving.Time_Step']
        self.dc_thresh = self.p['Shelving.dc_threshold']
        #self.disc = self.pv.get_parameter('StateReadout','state_readout_threshold')
        self.disc = 10

        # Get contexts for saving the data sets
        self.c_prob = self.cxn.context()
        self.c_hist = self.cxn.context()
        self.set_up_datavault()
       

    def run(self, cxn, context):

        '''
        Main loop ------ the old pulser calls program pulse sequence with the pulse sequence file which
        then pull the required paraemte

        rs from parameter vault ---- we now retrieve the parameter vault paramaters in
        the experiment file and pass them as arguments to the artiq server and the artiq experiment sequence
        '''
        t = np.linspace(float(self.start_time),float(self.stop_time),
                    int((abs(float(self.stop_time)-float(self.start_time))/float(self.step_time)) +1))
        exp_num = 0
        keys = list(self.p.keys())[:-1]
        keys.append('time')
        params = list(self.p.values())[:-1]
        params.append(0)
        for k in range(len(params)):
            params[k] = (float(params[k]))
        for i in range(len(t)):
            params[-1] = t[i]
            print(i)
            mean_pmt_count = 0.0
            self.artiq.program_pulse_sequence("shelving.py", keys, params)
            counts = self.artiq.get_exp_counts()

            try:
                counts = self.artiq.get_exp_counts()
                pmt_counts = counts[1]
                print(counts)
                print(pmt_counts)
            except:
                print('failed to get counts')
            mean_pmt_count = np.mean(pmt_counts)
            
            self.dv.add(t[i], mean_pmt_count, context = self.c_prob)
            data = np.column_stack((np.arange(len(pmt_counts)),pmt_counts))
            self.dv.add(data, context = self.c_hist)
            self.dv.add_parameter('hist'+str(i) + 'c' + str(int(self.cycles)), True, context = self.c_hist)
            exp_num += 1
        

    def set_up_datavault(self):
        # set up folder
        date = datetime.datetime.now()
        year  = str(date.year)
        month = '%02d' % date.month  # Padded with a zero if one digit
        day   = '%02d' % date.day    # Padded with a zero if one digit
        trunk = year + '_' + str(month) + '_' + str(day)

        # Open new data sets for prob and saving histogram data
        self.dv.cd(['',year,month,trunk],True, context = self.c_prob)
        dataset = self.dv.new('shelving_prob',[('time', 'us')], [('Probability', 'Probability', 'num')], context = self.c_prob)
        self.grapher.plot(dataset, 'shelving', False)
        # add dv params
        for parameter in self.p:
            self.dv.add_parameter(parameter, self.p[parameter], context = self.c_prob)


        self.dv.cd(['',year,month,trunk],True, context = self.c_hist)
        dataset1 = self.dv.new('shelving_hist',[('time', 'us')], [('Probability', 'Probability', 'num')], context = self.c_hist)
        # add dv params
        for parameter in self.p:
            self.dv.add_parameter(parameter, self.p[parameter], context = self.c_hist)
        self.dv.add_parameter('Readout Threshold', self.disc, context = self.c_hist)



if __name__ == '__main__':
    cxn = labrad.connect()
    scanner = cxn.scriptscanner
    exprt = shelving(cxn=cxn)
    ident = scanner.register_external_launch(exprt.name)
    exprt.execute(ident)
