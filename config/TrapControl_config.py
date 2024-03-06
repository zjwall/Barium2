class TrapControl_config(object):
    '''
    trap control client configuration file

    Attributes
    ----------
    info: dict
    {Parameter: (Rod1, Rod2, Rod3, Rod4))}
    {endCaps: (endCap 1, endCap 2)
    {einzel lens: (lens 1, lens 2)
    {Ablation loading delay:(time(usec))
    '''
    params = {'Frequency' :(1.099e6, 1.099e6, 1.099e6, 1.099e6),
            'Phase' :(15,170,0.5,38),
            'Voltage':(200, 1233, 200, 1233),
            'DC':(0,0,0,0),
            'HV':(900,920,1100,1100),
            'endCap':(.9,2.3),
            'eLens':(700,650),
            'Loading Time':(70)
            }
    '''
    IP address of the computer running the server
    '''
    ip = '10.97.111.3'
    
    '''
    IP address of the computer running the piezo controller for DC
    '''
    #dc_ip = '10.97.111.1'
    dc_ip = 'planetexpress'

    ''' Mapping of rods to channels

    rods: dict
    {rod:channel}

    '''

    rods = {'1':3, '2':1, '3':2, '4':0}
    dc_rods = {'1':3, '2':1, '3':2, '4':4}

    ''' Mapping of end caps to channels

    endCaps: dict
    {end cap : channel}

    '''
    endCaps = {'1':4, '2':5}

    ''' Mapping of einzel lens to channels

    einzel lens: dict
    {Elens : channel}

    '''
    eLens = {'1':6, '2':7}

