
from barium.lib.scripts.pulse_sequences.pulse_sequence import pulse_sequence


class test_sequence(pulse_sequence):

    required_parameters = [
                      ('TestSequence', 'Time'),
                      ('TestSequence', 'random'),
                      ('TestSequence', 'Pulse_Number')
                          ]

        
