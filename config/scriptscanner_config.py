class config(object):

    """
    scriptscanner config object for the barium experiment.
    """
    # Folder names within the experiments folder that holder experiments
    exps = 'barium.lib.scripts.experiments.'

    # list in the format (import_path, class_name)
    scripts = [#(exps + 'optical_pumping.optical_pumping', 'optical_pumping'),
               #(exps + 'rabi_flopping.rabi_flopping','rabi_flopping'),
               #(exps + 'microwave_sweep.microwave_sweep','microwave_sweep'),
               #(exps + 'bright_state_detection.bright_state_detection', 'bright_state_detection'),
               #(exps + 'ramsey.ramsey','ramsey'),
               (exps + 'shelving.shelving','shelving'),
               (exps + 'flourescence_detection.flourescence_detection','flourescence_detection'),
               (exps + 'tickle_sweep.tickle_sweep','tickle_sweep'),
               ]

    # This allows running multiple experiments at the same time. Use the name defined
    # below the class definition i.e. name = "exp name"
    allowed_concurrent = {}
    allowed_concurrent['Laser Monitor'] = ['Laser Monitor', 'Probe Line Scan']


launch_history = 1000
