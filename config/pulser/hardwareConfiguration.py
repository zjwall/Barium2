class channelConfiguration(object):
    """
    Stores complete configuration for each of the channels
    """
    def __init__(self, channelNumber, ismanual, manualstate,  manualinversion, autoinversion):
        self.channelnumber = channelNumber
        self.ismanual = ismanual
        self.manualstate = manualstate
        self.manualinv = manualinversion
        self.autoinv = autoinversion

class ddsConfiguration(object):
    """
    Stores complete configuration of each DDS board
    """
    def __init__(self, address, allowedfreqrange, allowedamplrange, frequency, amplitude, **args):
        self.channelnumber = address
        self.allowedfreqrange = allowedfreqrange
        self.allowedamplrange = allowedamplrange
        self.frequency = frequency
        self.amplitude = amplitude
        self.state = True
        self.boardfreqrange = args.get('boardfreqrange', (0.0, 2000.0)) # input reference frequency for the DDS
        self.boardramprange = args.get('boardramprange', (0.000113687, 7.4505806))
        self.board_amp_ramp_range = args.get('board_amp_ramp_range', (0.00174623, 22.8896))
        self.boardamplrange = args.get('boardamplrange', (-48.0, 6.0))
        self.boardphaserange = args.get('boardphaserange', (0.0, 360.0))
        self.off_parameters = args.get('off_parameters', (0.0, -48.0))
        self.phase_coherent_model = args.get('phase_coherent_model', True)
        self.remote = args.get('remote', False)
        self.name = None #will get assigned automatically

class remoteChannel(object):
    def __init__(self, ip, server, **args):
        self.ip = ip
        self.server = server
        self.reset = args.get('reset', 'reset_dds')
        self.program = args.get('program', 'program_dds')

class hardwareConfiguration(object):
    channelTotal = 32
    timeResolution = '40.0e-9' #seconds
    timeResolvedResolution = 10.0e-9
    maxSwitches = 1022
    resetstepDuration = 3 #duration of advanceDDS and resetDDS TTL pulses in units of timesteps
    collectionTimeRange = (0.010, 5.0) #range for normal pmt counting
    sequenceTimeRange = (0.0, 85.0) #range for duration of pulse sequence
    isProgrammed = False
    sequenceType = None #none for not programmed, can be 'one' or 'infinite'
    collectionMode = 'Normal' #default PMT mode
    collectionTime = {'Normal':0.100,'Differential':0.100} #default counting rates
    okDeviceID = 'Pulser2'
    #okDeviceFile = 'photon_2015_06_10.bit'
    okDeviceFile = 'photon_2015_7_13.bit'
    lineTriggerLimits = (0, 15000)#values in microseconds
    secondPMT = False
    DAC = False

    #name: (channelNumber, ismanual, manualstate,  manualinversion, autoinversion)
    channelDict = {
           # Internal866 is in pulser firmware, this is the required channel name.
                   'Internal866':channelConfiguration(0, False, False, False, True), ## camera
                   '866DP':channelConfiguration(1, False, False, True, False), # 866DP is in pulser firmware, this is the required channel name.
                   'TTL2':channelConfiguration(2, False, False, False, True), # manual compatible, reserve for 650 Doppler cooling, autoinvert true so default cool
                   'TTL3':channelConfiguration(3, False, False, False, True), # manual compatible, reserve for 493 Doppler cooling, autoinvert true so default cool
                   'TTL4':channelConfiguration(4, False, False, False, False), # manual compatible, use for microwave switch
                   'PMT/Camera':channelConfiguration(5, True, False, False, False), # manual compatible, Use for pmt/camera switch
                   'TTL6':channelConfiguration(6, False, False, False, True), # manual compatible, 
                   'TTL7':channelConfiguration(7, False, False, False, False), # manual compatible, Use for 455 AOM RF Switch
                   'TTL8':channelConfiguration(8, False, False, False, False), # manual compatible, Use for 614 AOM RF switch
                   'TTL9':channelConfiguration(9, False, False, False, False), # manual compatible, 1762 EOM
                   'TTL10':channelConfiguration(10, False, False, False, True), # manual compatible # 493 rf switch
                   'TTL11':channelConfiguration(11, False, False, False, False), # manual compatible # use for optical pumping
                   'TTL12':channelConfiguration(12, False, False, False, False),  #BABD Channel
                   'TTL13':channelConfiguration(13, False, False, False, False),
                   'TTL14':channelConfiguration(14, False, False, False, False),
                   'TTL15':channelConfiguration(15, False, False, False, False),
                   'DiffCountTrigger':channelConfiguration(16, False, False, False, False),
                   'TimeResolvedCount':channelConfiguration(17, False, False, False, False), # needed to activate time tagged photon counting
                   'AdvanceDDS':channelConfiguration(18, False, False, False, False),
                   'ResetDDS':channelConfiguration(19, False, False, False, False),

                   'ReadoutCount':channelConfiguration(20, False, False, False, False), ### triggering for analog board, needed to count photons without time tagging.
                   'TTL21':channelConfiguration(21, False, False, False, False), ### triggering for analog board
                   'TTL22':channelConfiguration(22, True, True, False, False),
                   'TTL23':channelConfiguration(23, True, True, False, False),
                   'TTL24':channelConfiguration(24, False, False, False, False), ## for plotting the clock purpose only
                   'TTL25':channelConfiguration(25, False, False, False, False), # reserve for weak probe line scan 650
                   'TTL26':channelConfiguration(26, False, False, False, False),
                   'TTL27':channelConfiguration(27, False, False, False, False), 
                   'TTL28':channelConfiguration(28, False, False, False, False),
                   'TTL29':channelConfiguration(29, False, False, False, False),
                   'TTL30':channelConfiguration(30, False, False, False, False),
                   'TTL31':channelConfiguration(31, False, True, False, False),
                }
    #address, allowedfreqrange, allowedamplrange, frequency, amplitude, **args):
    ddsDict =   {
                 '493nm':ddsConfiguration(    0,  (40.0,400.0),   (-48.0,6.0),  125.0,   -48.0),
                 'Microwaves':ddsConfiguration(1,  (1,1000.0),   (-48.0,-1.0), 375.0,   -48.0),
                 'LF DDS':ddsConfiguration(    2,  (.001,1000.0),   (-48.0,-2.0),  26.286,   -5.0),
                 '614nm':ddsConfiguration(    3,  (1,1000.0),   (-48.0,2.0),  320,   -1.0),
                 '650nm':ddsConfiguration(    4,  (1,1000.0),   (-48.0,6.0),  125.0,   1.0),
                 '780_1nm':ddsConfiguration(10,  (1,1000.0),   (-48.0,-16.0),  80.0,   -48.0),
                 '1762nm':ddsConfiguration(12,  (1,1000.0),   (-48.0,-8.0),  250.0,   -48.0),
                }
    remoteChannels = {
}
