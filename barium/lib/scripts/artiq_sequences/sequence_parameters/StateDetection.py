
from barium.lib.scripts.pulse_sequences.pulse_sequence import pulse_sequence


class StateDetection(pulse_sequence):

    required_parameters = [
                      ('StateDetection', 'duration')
                          ]
