class multiplexer_config(object):
##    '''
##    multiplexer client configuration file
##
##    Attributes
##    ----------
##    info: dict
##    {channel_name: (Multiplexer Channel, hint, display_location (column,row), stretched, display PID,
##    DAC Channel (0 unassigned)), Rail Volatages), display interferometer (bool)}
##
##    '''
    stretched = False
    displayPID = True
    info = {'493nm' :(1, '607.425680', (0,1), stretched, displayPID, 1,[-7,7], False),
            '650nm' :(15, '461.311355', (0,2), stretched, displayPID, 2,[-5,5],False),
            '585nm' :(2, '512.001400', (0,3), stretched, displayPID, 0,[-5,5],False),
            '455nm' :(7,'658.115671', (4,1), stretched, displayPID, 0,[-5,5],False),
            '614nm' :(5,'487.989370', (4,2), stretched, displayPID, 0,[-5,5],False),
            }

##    '''
##    info: dict
##    {channel_name: (Multiplexer Channel, hint, display_location (column,row), gain,
##    DAC Channel (0 unassigned)), Rail Volatages, locked, output voltage)}
##    '''
    single_lock = {
            '455nm' :(2, '658.116220', (0,3), .001,  7,[0,30], 0, 0),
            '585nm' :(16, '512.141000', (0,3), .001,  6,[0,30], 0, 0),
                   }
##    '''
##    name of cert for the wavemeter computer
##    '''
    ip = '10.97.109.81'

    #ip = '10.97.112.2'
