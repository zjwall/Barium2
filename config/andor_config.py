class andor_config(object):

    '''
    path to atmcd64d_legacy.dll SDK library
    '''
    path_to_dll = 'C:\\Program Files\\Andor SOLIS\\atmcd64d_legacy.dll'
    #default parameters
    set_temperature = -60 #degrees C
    read_mode = 'Image'
    acquisition_mode = 'Single Scan'
    trigger_mode = 'Internal'
    exposure_time = 0.200 #seconds
    binning = [1, 1] #numbers of pixels for horizontal and vertical binning
    shutter_mode = 'Auto'

    image_path = 'H:/Image_Data/'
    save_in_sub_dir = True
    save_format = "csv" # options are tsv, csv, bin
    save_header = False
