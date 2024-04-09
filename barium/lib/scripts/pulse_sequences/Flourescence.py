
from barium.lib.scripts.pulse_sequences.pulse_sequence import pulse_sequence


class flourescence(pulse_sequence):

    required_parameters = [
                      ('Flourescence', 'Cycles'),
                      ('Flourescence', 'Delay_Time')
                          ]

        
