class shutter_config(object):
    '''
    configuration file for arduino switch client
    info is the configuration dictionary in the form
    {channel_name: (port, display_location, inverted, enable port)), }
    '''
    info = {'Protection Beam': (9, (0,1), True, 5),
            '1762 Laser': (10, (0,2), True, 6),
            }
