# Copyright (C) 2022 Zach Wall

"""
### BEGIN NODE INFO
[info]
name = Artiq Server

version = 1.0
description =

[startup]
cmdline = %PYTHON% %FILE%
timeout = 20
[shutdown]
message = 987654321
timeout = 5
### END NODE INFO
"""


import os
from labrad.server import LabradServer, setting, Signal
from labrad import types as T
from twisted.internet.defer import returnValue, inlineCallbacks
from labrad.support import getNodeName
from artiq_api import ARTIQ_api
import numpy as np
from artiq_config import config

TTLSIGNAL_ID = 828176
DACSIGNAL_ID = 828175
DDSSIGNAL_ID = 828172

DDB_FILEPATH = 'C:\\Users\\barium133\\Code\\barium\\lib\\servers\\Artiq\\device_db.py'

class Artiq_Server(LabradServer):

    name = 'Artiq Server'

    ddsChanged = Signal(DDSSIGNAL_ID, 'signal: dds changed', '(ssv)')
    ttlChanged = Signal(TTLSIGNAL_ID, 'signal: ttl changed', '(sb)')
    dacChanged = Signal(DACSIGNAL_ID, 'signal: dac changed', '(ssv)')

    @inlineCallbacks
    def initServer(self):
        self.api = ARTIQ_api(DDB_FILEPATH)

        #initialize DAC required if device restarted
        yield self.api.initializeDAC()
        yield self.set_Devices()
        self.setup2()

    def set_Devices(self):
        """
        Get the list of devices in the ARTIQ box.
        """
        dds_tmp = list(self.api.dds_list.values())[0]
        self.ca = dds_tmp.amplitude_to_asf(1.0)
        self.fa = dds_tmp.frequency_to_ftw(1.0)*1e6
        self.dac_vals = [0]*32
        self.dac_state = [False]*32
        self.TTL_state = [False]*24
        self.dds_params = {}
        self.ttlout_list = list(self.api.ttlout_list.keys())
        self.ttlin_list = list(self.api.ttlin_list.keys())
        self.dds_list = list(self.api.dds_list.keys())
        for key in self.dds_list:
            self.dds_params[key] = [100.0,0.0,False,31.5]

    @inlineCallbacks
    def setup(self):
        for i in range(4,24):
            yield self.api.setTTL('ttl'+str(i),False)
        for i in range(32):
            yield self.api.setZotino(i, float(0.0))
            
    @inlineCallbacks
    def setup2(self):
        for i in range(12):
            if i in config.DDS_dict.keys():
                dds_name  = self.dds_list[i]
                freq = float(config.DDS_dict[i][1])
                amp = float(config.DDS_dict[i][2])
                att = float(config.DDS_dict[i][3])
                state = config.DDS_dict[i][4]
                self.dds_params[dds_name][0] = freq
                self.dds_params[dds_name][1] = amp
                self.dds_params[dds_name][2] = state
                self.dds_params[dds_name][3] = att
                yield self.api.setDDS(dds_name, freq, amp)
                yield self.api.setDDSatt(dds_name, att)
                yield self.api.toggleDDS(dds_name, state)

            
        
    # CORE
    @setting(21, returns='*s')
    def get_Devices(self, c):
        """
        Returns a list of ARTIQ devices.
        """
        return list(self.api.device_db.keys())

    @setting(31, dataset_name='s', returns='?')
    def get_Dataset(self, c, dataset_name):
        """
        Returns a dataset.
        Arguments:
            dataset_name    (str)   : the name of the dataset
        Returns:
            the dataset
        """
        return self.datasets.get(dataset_name, archive=False)


    @setting(421, dac_num='i', value='v', units='s', returns='')
    def set_dac(self, c, dac_num, value, units='mu'):
        """
        Manually set the voltage of a DAC channel.
        Arguments:
            dac_num (int)   : the DAC channel number
            value   (float) : the value to write to the DAC register
            units   (str)   : the voltage units, either 'mu' or 'v'
        """
        voltage_max = 10.0
        # check that dac channel is valid
        if (dac_num > 31) or (dac_num < 0):
            raise Exception('Error: device does not exist.')
        # check that units and voltage are valid
        if value > voltage_max or value < -voltage_max:
            raise Exception('Error: voltage out of range')


        self.dac_vals[dac_num] = float(value)
        if self.dac_state[dac_num]:
            yield self.api.setZotino(dac_num, float(value))


    @setting(431, dac_num='i', returns='i')
    def read_dac(self, c, dac_num):
        """
        Read the value of a DAC register.
        Arguments:
            dac_num (int)   : the dac channel number
            param   (float) : the register to read from
        """
        if (dac_num > 31) or (dac_num < 0):
            raise Exception('Error: device does not exist.')

        reg_val = yield self.api.readZotino(dac_num)

        returnValue(reg_val)

    @setting(441, dac_num = 'i', returns = 'v')
    def get_dac_val(self, c, dac_num):
        return(self.dac_vals[dac_num])

    @setting(451, dac_num = 'i', returns = '')
    def set_dac_state(self, c, dac_num, state):
        if state:
            self.dac_state[dac_num] = True
            yield self.api.setZotino(dac_num, self.dac_vals[dac_num])
        else:
            self.dac_state[dac_num] = False
            yield self.api.setZotino(dac_num, float(0.0))

    @setting(461, dac_num = 'i', returns = 'b')
    def get_dac_state(self, c, dac_num):
        return(self.dac_state[dac_num])

    # TTL
    @setting(211, returns='*s')
    def list_ttl(self, c):
        """
        Lists all available TTL channels.
        Returns:
                (*str)  : a list of all TTL channels.
        """
        return self.ttlout_list + self.ttlin_list

    @setting(221, ttl_name='i', state=['b', 'i'], returns='')
    def set_ttl(self, c, ttl_name, state):
        """
        Manually set a TTL to the given state. TTL can be of classes TTLOut or TTLInOut.
        Arguments:
            ttl_name    (str)           : name of the ttl
            state       [bool, int]     : ttl power state
        """
        if 'ttl'+ str(ttl_name) not in self.ttlout_list:
            raise Exception('Error: devi6ce does not exist.')
        if (type(state) == int) and (state not in (0, 1)):
            raise Exception('Error: invalid state.')
        self.TTL_state[ttl_name] = state
        yield self.api.setTTL('ttl'+ str(ttl_name), state)
        self.ttlChanged(('ttl'+ str(ttl_name), state))

    @setting(231, ttl_name='i', time='i', returns='')
    def pulse_ttl(self, c, ttl_name, time):
        """
        Manually pulse  a TTL for a given time."""
        
        if 'ttl'+ str(ttl_name) not in self.ttlout_list:
            raise Exception('Error: devi6ce does not exist.')
        if (time < 1) or time > 1000:
            raise Exception('Error: invalid time.')
        yield self.api.pulseTTL('ttl'+ str(ttl_name), time)
        
    @setting(232, time_1='i', time_2='i',returns='')
    def pulse_ablation(self, c, time_1, time_2):
        """
        Manually pulse the trap and the ablation laser
        time_1 is time trap is off
        time_2 is start time of ablation pulse
        """
        
        if (time_1 < 1) or time_1 > 1000:
            raise Exception('Error: invalid time.')
        yield self.api.ablate('ttl'+ str(11), 'ttl' + str(8), time_1, time_2)


    @setting(233, time_1='i', time_2='i', time_3 = 'i', returns='')
    def pulse_ablation_endcaps(self, c, time_1, time_2,time_3):
        """
        Manually pulse the trap and the ablation laser and the dac
        time_1 is time trap is off
        time_2 is start time of ablation pulse
        """
        
        if (time_1 < 1) or time_1 > 1000:
            raise Exception('Error: invalid time.')
        yield self.api.ablate_endcaps('ttl'+ str(11), 'ttl' + str(8), time_1, time_2,time_3)


    @setting(234, time_1='i', returns='')
    def pulse_endcaps(self, c, time_1):
        """
        Manually pulse the trap encaps
        """
        if (time_1 < 1) or time_1 > 1000:
            raise Exception('Error: invalid time.')
        yield self.api.pulse_endcaps('ttl' + str(8), time_1)
        

    @setting(222, ttl_name='i', returns='b')
    def get_ttl(self, c, ttl_name):
        """
        Read the power state of a TTL. TTL must be of class TTLInOut.
        Arguments:
            ttl_name    (str)   : name of the ttl
        Returns:
                        (bool)  : ttl power state
        """
        if 'ttl'+ str(ttl_name) not in self.ttlin_list:
            raise Exception('Error: device does not exist.')
        state = yield self.api.getTTL('ttl'+ str(ttl_name))
        returnValue(bool(state))

    @setting(223, TTL_num = 'i', returns = 'b')
    def get_ttl_state(self, c, TTL_num):
        return(self.TTL_state[TTL_num])


    # DDS
    @setting(311, returns='*s')
    def list_dds(self, c):
        """
        Get the list of available DDS (AD5372) channels.
        Returns:
            (*str)  : the list of dds names
        """
        dds_list = yield self.api.dds_list.keys()
        #dds_list = yield self.api.urukul_list.keys()
        returnValue(list(dds_list))

    @setting(301, returns='*s')
    def list_urukul(self, c):
        """
        Get the list of available DDS (AD5372) channels.
        Returns:
            (*str)  : the list of dds names
        """
        ur_list = yield self.api.urukul_list.keys()
        #dds_list = yield self.api.urukul_list.keys()
        returnValue(list(ur_list))

    @setting(321, dds_name='s', returns='')
    def initialize_dds(self, c, dds_name):
        """
        Resets/initializes the DDSs.
        Arguments:
            dds_name    (str)   : the name of the dds
        """
        if dds_name not in self.dds_list:
            raise Exception('Error: device does not exist.')
        yield self.api.initializeDDS(dds_name)

        
    @setting(323, dds_name='s', freq='v', returns='')
    def set_dds_freq(self, c, dds_name, freq):
        """
        Manually set the frequency of a DDS.
        Arguments:
            dds_name    (str)   : the name of the dds
            freq        (float) : the frequency in Hz
        """
        if dds_name not in self.dds_list:
            raise Exception('Error: device does not exist.')
        if freq > 500 or freq < 0:
            raise Exception('Error: frequency must be within [0 Hz, 400 MHz].')
        amp = self.dds_params[dds_name][1]
        self.dds_params[dds_name][0] = float(freq)
        yield self.api.setDDS(dds_name, float(freq), float(amp))
        self.ddsChanged((dds_name, 'freq', float(freq)))

    @setting(324, dds_name='s', amp='v', returns='')
    def set_dds_amp(self, c, dds_name, amp):
        """
        Manually set the amplitude of a DDS.
        Arguments:
            dds_name    (str)   : the name of the dds
            ampl        (float) : the fractional amplitude
        """
        if dds_name not in self.dds_list:
            raise Exception('Error: device does not exist.')
        if amp > 1 or amp < 0:
            raise Exception('Error: amplitude must be within [0, 1].')
        freq = self.dds_params[dds_name][0]
        self.dds_params[dds_name][1] = float(amp)
        yield self.api.setDDS(dds_name, float(freq), float(amp))
        self.ddsChanged((dds_name, 'amp', float(amp)))

    @setting(334, dds_name='s', att='v', returns='')
    def set_dds_att(self, c, dds_name, att):
        """
        Manually set the amplitude of a DDS.
        Arguments:
            dds_name    (str)   : the name of the dds
            ampl        (float) : the fractional amplitude
        """
        if dds_name not in self.dds_list:
            raise Exception('Error: device does not exist.')
        if att > 31.5 or att < 0:
            raise Exception('Error: attenuation must be within [0, 31.5].')
        self.dds_params[dds_name][3] = float(att)
        yield self.api.setDDSatt(dds_name, float(att))
        self.ddsChanged((dds_name, 'att', float(att)))
    

    @setting(322, dds_name='s', state=['b', 'i'], returns='')
    def toggle_dds(self, c, dds_name, state):
        """
        Manually toggle a DDS via the RF switch
        Arguments:
            dds_name    (str)           : the name of the dds
            state       [bool, int]     : power state
        """
        if dds_name not in self.dds_list:
            raise Exception('Error: device does not exist.')
        if (type(state) == int) and (state not in (0, 1)):
            raise Exception('Error: device does not exist.')
        self.dds_params[dds_name][2] = state
        yield self.api.toggleDDS(dds_name, state)
        
    @setting(331, dds_name='s', returns='s')
    def readDDS(self, c, dds_name):
        """
        Read the value of a DDS register.
        Arguments:
            dds_name    (str)   : the name of the dds
            addr        (int)   : the address to read from
            length      (int)   : how many bits to read
        Returns:
            (word)  : the register value
        """
        if dds_name not in self.dds_list:
            raise Exception('Error: device does not exist.')

        reg_val = yield self.api.getDDS(dds_name)
        returnValue(str(reg_val[0]/float(self.fa)) + ' ' + str(float(reg_val[1])/float(self.ca)) + ' ' + str(reg_val[2]))


    @setting(351, dds_name = 's', returns = 'v')
    def get_dds_freq(self, c, dds_name):
        return(self.dds_params[dds_name][0])
    
    @setting(361, dds_name = 's', returns = 'v')
    def get_dds_amp(self, c, dds_name):
        return(self.dds_params[dds_name][1])

    @setting(371, dds_name = 's', returns = 'b')
    def get_dds_state(self, c, dds_name):
        return(self.dds_params[dds_name][2])

    @setting(381, dds_name = 's', returns = 'v')
    def get_dds_att(self, c, dds_name):
        return(self.dds_params[dds_name][3])

    @setting(391, dds_name = 's', returns = 'v')
    def read_dds_att(self, c, dds_name):
        return self.api.getDDSatt(dds_name)


    @setting(401, time_us='i', trials='i', returns='*v')
    def ttl_count_list(self, c, time_us=100, trials=10):
        """
        Read the number of counts from a TTL in a given time and
            averages it over a number of trials.
            TTL must be of class EdgeCounter.
        Arguments:
            ttl_name    (str)   : name of the ttl
            time_us     (int)   : number of seconds to count for
            trials      (int)   : number of trials to average counts over
        Returns:
                        (float) : averaged number of ttl counts
        """

        counts_list = yield self.api.counterTTL('PMT', time_us, trials)
        returnValue(counts_list)

            
    @setting(1000, exp_file = 's', keys = '*s', params = '*v')
    def program_pulse_sequence(self, c, exp_file, keys, params):
        self.api.input_pulse_sequence("C:\\Users\\barium133\Code\\barium\\lib\\scripts\\artiq_sequences\\" + exp_file,keys,params)

    @setting(1100, returns = '**v')
    def get_exp_counts(self, c):
        pmt_counts = self.api.get_temp_counts()
        return(pmt_counts)
 
if __name__ == "__main__":
    from labrad import util
    util.runServer(Artiq_Server())
