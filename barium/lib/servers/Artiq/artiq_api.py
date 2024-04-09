# Copyright (C) 2022 Zach Wall

from artiq.frontend.artiq_run import _build_experiment, get_argparser, DummyScheduler, DummyCCB
from artiq.master.databases import DeviceDB, DatasetDB
from artiq.master.worker_db import DeviceManager, DatasetManager


from artiq.experiment import *
from artiq.master.databases import DeviceDB
from artiq.master.worker_db import DeviceManager
from artiq.coredevice.urukul import CPLD as UrukulCPLD
from artiq.coredevice.ad9910 import AD9910
import numpy as np
from builtins import ConnectionAbortedError, ConnectionResetError


class ARTIQ_api(object):

    def autoreload(func):
        """
        A decorator for non-kernel functions that attempts to reset
        the connection to artiq_master if we lost it.
        """
        def inner(self, *args, **kwargs):
            try:
                res = func(self, *args, **kwargs)
                return res
            except (ConnectionAbortedError, ConnectionResetError) as e:
                try:
                    print('Connection aborted, resetting connection to artiq_master...')
                    self.reset()
                    res = func(self, *args, **kwargs)
                    return res
                except Exception as e:
                    raise e
        return inner

    
    def __init__(self, ddb_filepath):
        devices = DeviceDB(ddb_filepath)
        self.ddb_filepath = ddb_filepath
        self.device_manager = DeviceManager(devices,
                              virtual_devices={"scheduler": DummyScheduler(),
                                            "ccb": DummyCCB()})
        self.device_db = devices.get_device_db()
        d = 'C:\\Users\\barium133\\Code\\barium\\lib\\servers\\Artiq\\dataset_db.pyon'
        dataset_db = DatasetDB(d)
        self.dataset_mgr = DatasetManager(dataset_db)
        self._getDevices()

    def reset(self):
        """
        Reestablishes a connection to artiq_master.
        """
        devices = DeviceDB(self.ddb_filepath)
        self.device_manager = DeviceManager(devices,
                           virtual_devices={"scheduler": DummyScheduler(),
                                            "ccb": DummyCCB()})
        self.device_db = devices.get_device_db()
        self._getDevices()

    def _getDevices(self):
        """
        Gets necessary device objects.
        """
        # get core
        self.core = self.device_manager.get("core")
        self.core_dma = self.device_manager.get("core_dma")
        # store devices in dictionary where device
        # name is key and device itself is value
        self.ttlout_list = {}
        self.ttlin_list = {}
        self.ttlcounter_list = {}
        self.dds_list = {}
        self.urukul_list = {}
        self.zotino = None
        self.fastino = None
        self.dacType = None
        self.sampler = None
        self.phaser = None
        self.temp_pmt_counts = []
        # assign names and devices
        for name, params in self.device_db.items():
            # only get devices with named class
            if 'class' not in params:
                continue
            # set device as attribute
            devicetype = params['class']
            device = self.device_manager.get(name)
            if devicetype == 'TTLInOut':
                self.ttlin_list[name] = device
            elif devicetype == 'TTLOut':
                self.ttlout_list[name] = device
            elif devicetype == 'AD9910':
                self.dds_list[name] = device
            elif devicetype == 'CPLD':
                self.urukul_list[name] = device
            elif devicetype == 'Zotino':
                # need to specify both device types since
                # all kernel functions need to be valid
                self.zotino = device
                self.fastino = device
                self.dacType = devicetype
            elif devicetype == 'Fastino':
                self.fastino = device
                self.zotino = device
                self.dacType = devicetype
            elif devicetype == 'Sampler':
                self.sampler = device
            elif devicetype == 'Phaser':
                self.phaser = device
            elif devicetype == 'EdgeCounter':
                self.ttlcounter_list[name] = device

                
    def _initializeDevices(self):
        """
        Initialize devices that need to be initialized.
        """
        # initialize DDSs
        self.initializeDDSAll()
        # one-off device init
        self.initializeDAC()
                

    # DAC/ZOTINO
    @autoreload
    def initializeDAC(self):
        self._initializeDAC()

    @kernel
    def _initializeDAC(self):
        """
        Initialize the DAC.
        """
        self.core.reset()
        self.zotino.init()


    @autoreload
    def setZotino(self, channel_num, volt_mu):
        self._setZotino(channel_num, volt_mu)

    @kernel
    def _setZotino(self, channel_num, volt_mu):
        """
        Set the voltage of a DAC register.
        """
        self.core.reset()
        delay(200*us)
        self.zotino.write_dac(channel_num, volt_mu)
        self.zotino.load()

    @autoreload
    def readZotino(self, channel_num):
        return self._readZotino(channel_num)

    @kernel
    def _readZotino(self, channel_num):
        """
        Read the value of one of the DAC registers.
        :param channel_num: Channel to read from
        :param address: Register to read from
        :return: the value of the register
        """
        self.core.reset()
        reg_val = self.zotino.read_reg(channel_num)
        return reg_val


    # TTL

    
    @autoreload
    def setTTL(self, ttlname, state):
        """
        Manually set the state of a TTL.
        """
        try:
            dev = self.ttlout_list[ttlname]
        except KeyError:
            raise Exception('Invalid device name.')
        self._setTTL(dev, state)

    @kernel
    def _setTTL(self, dev, state):
        self.core.reset()
        if state:
            dev.on()
        else:
            dev.off()

    def getTTL(self, ttlname):
        """
        Manually set the state of a TTL.
        """
        try:
            dev = self.ttlin_list[ttlname]
        except KeyError:
            raise Exception('Invalid device name.')
        self._getTTL(dev)

    @kernel
    def _getTTL(self, dev):
        self.core.reset()
        return dev.sample_get_nonrt()


    @autoreload
    def pulseTTL(self, ttlname, time):
        """
        Manually pulse a TTL.
        """
        try:
            dev = self.ttlout_list[ttlname]
        except KeyError:
            raise Exception('Invalid device name.')
        self._pulseTTL(dev, time)

    @kernel
    def _pulseTTL(self, dev, time):
        self.core.reset()
        dev.pulse(time*us)


    @autoreload
    def ablate(self, ttlname_1, ttlname_2, time_1, time_2):
        """
        Manually pulse a two TTL's for trap rf and ablation pulse.
        """
        try:
            dev1 = self.ttlout_list[ttlname_1]
        except KeyError:
            raise Exception('Invalid device name.')
        try:
            dev2 = self.ttlout_list[ttlname_2]
        except KeyError:
            raise Exception('Invalid device name.')
        self._ablate(dev1, dev2, time_1, time_2)

    @kernel
    def _ablate(self, dev1, dev2, time_1, time_2):
        self.core.reset()
        with parallel:
            dev1.pulse(time_1*us)
            with sequential:
                delay(time_2*us)
                dev2.pulse(3*us)


    @autoreload
    def ablate_endcaps(self, ttlname_1, ttlname_2, time_1, time_2,time_3):
        """
        Manually pulse a two TTL's for trap rf and ablation pulse.
        """
        try:
            dev1 = self.ttlout_list[ttlname_1]
        except KeyError:
            raise Exception('Invalid device name.')
        try:
            dev2 = self.ttlout_list[ttlname_2]
        except KeyError:
            raise Exception('Invalid device name.')

        self._ablate_endcaps(dev1, dev2, time_1, time_2,time_3)

    @kernel
    def _ablate_endcaps(self, dev1, dev2, time_1, time_2,time_3):
        self.core.reset()
        with parallel:
            dev1.pulse(time_1*us)
            with sequential:
                delay(time_2*us)
                dev2.pulse(3*us)
            with sequential:
                self.zotino.set_dac([0], [9])
                delay(time_3*us)
                self.zotino.set_dac([9], [9])
                
        



    @autoreload
    def pulse_endcaps(self, ttlname_3, time_1):
        """
        Manually pulse a two TTL's for trap rf and ablation pulse.
        """
        try:
            dev1 = self.ttlout_list[ttlname_3]
        except KeyError:
            raise Exception('Invalid device name.')
        self._pulse_endcaps(dev1, time_1)

    @kernel
    def _pulse_endcaps(self,dev1, time_1):
        self.core.reset()
        with parallel:
            dev1.pulse(3*us)
            self.zotino.set_dac([0], [9])
        delay(time_1*us)
        self.zotino.set_dac([9], [9])



        
    # DDS

    @autoreload
    def initializeDDSAll(self):
        # initialize urukul cplds as well as dds channels
        device_list = list(self.urukul_list.values())
        for device in device_list:
            self._initializeDDS(device)
        dev_list2 = list(self.dds_list.values())
        for device in dev_list2:
            self._initializeDDS(device)
    @autoreload
    def initializeDDS(self, dds_name):
        dev = self.dds_list[dds_name]
        self._initializeDDS(dev)

    @kernel
    def _initializeDDS(self, dev):
        self.core.reset()
        dev.init()
        
        
    @autoreload
    def setDDS(self, dds_name, freq, amp):
        """
        Manually set the frequency, amplitude, or phase of a DDS channel.
        """
        dev = self.dds_list[dds_name]
        self._setDDS(dev,freq,amp)

    @kernel
    def _setDDS(self,dev,freq,amp):
        self.core.reset()
        delay(30*us)
        dev.set(freq*MHz, amplitude=amp)

    @autoreload
    def setDDSatt(self, dds_name, att):
        """
        Set the DDS attenuation.
        """
        dev = self.dds_list[dds_name]
        # get channel number of dds
        chan = dev.chip_select - 4
        self._setDDSatt(dev.cpld, chan, att)

    @kernel
    def _setDDSatt(self, cpld, chan, att):
        self.core.reset()
        delay(30*us)
        cpld.set_att(chan, att)
    
    @autoreload
    def toggleDDS(self, dds_name, state):
        dev = self.dds_list[dds_name]
        self._toggleDDS(dev, state)

    @kernel
    def _toggleDDS(self, dev, state):
        self.core.reset()
        if state == True:
            dev.sw.on()
        else:
            dev.sw.off()

    def getDDS(self, dds_name):
        """
        Get the frequency, amplitude, and phase values
        (in machine units) of a DDS channel.
        """
        dev = self.dds_list[dds_name]
        # read in waveform values
        profiledata = self._readDDS64(dev, 0x0E)
        # separate register values into ftw, asf, and pow
        ftw = profiledata & 0xFFFFFFFF
        pow = ((profiledata >> 32) & 0xFFFF)
        asf = (profiledata >> 48)
        # asf = -1 means amplitude has not been set
        if asf < 0:
            asf = 0
        else:
            asf &= 0x3FFF
        return np.int32(ftw), np.int32(asf), np.int32(pow)
    
    
    def getDDSatt(self, dds_name):
        dev = self.dds_list[dds_name]
        chan =dev.chip_select-4
        return self._getDDSatt(dev.cpld, chan)
        
    @kernel
    def _getDDSatt(self, cpld, chan):
        self.core.reset()
        return cpld.get_channel_att(chan)

    
    @kernel
    def _readDDS64(self, dev, reg):
        self.core.reset()
        return dev.read64(reg)

    @autoreload
    def counterTTL(self, ttlname, time, trials):
        """
        Get the number of TTL input events for a given time, averaged over a number of trials.
        """
        try:
            dev = self.ttlcounter_list[str(ttlname) + '_counter']
        except KeyError:
            raise Exception('Invalid device name.')

        # create holding structures for counts
        setattr(self, "ttl_counts_array", np.zeros(trials))
        # get counts
        self._counterTTL(dev, time, trials)
        # delete holding structure
        tmp_arr = self.ttl_counts_array
        delattr(self, "ttl_counts_array")
        return tmp_arr


    @kernel
    def _counterTTL(self, dev, time, trials):
        self.core.reset()
        for i in range(trials):
            self.core.break_realtime()
            dev.gate_rising(time*us)
            self._recordTTLCounts(dev.fetch_count(), i)
        

    @rpc(flags={"async"})
    def _recordTTLCounts(self, value, index):
        """
        Records values via rpc to minimize kernel overhead.
        """
        self.ttl_counts_array[index] = value

    
    def input_pulse_sequence(self, exp_file, keys, params):
        """
        Records values via rpc to minimize kernel overhead.
        """
        args = get_argparser().parse_args({exp_file})
        exp_inst=_build_experiment(self.device_manager, self.dataset_mgr, args)
        exp_inst.prepare()
        exp_inst.build()
        exp_inst.set_vals(keys, params)
        exp_inst.run()
        self.temp_pmt_counts = exp_inst.get_counts()
        

    def get_temp_counts(self):
        return self.temp_pmt_counts
        
    
