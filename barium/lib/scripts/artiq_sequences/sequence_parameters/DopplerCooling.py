
from barium.lib.scripts.pulse_sequences.pulse_sequence import pulse_sequence


class DopplerCooling(pulse_sequence):

    required_parameters = [
                      ('DopplerCooling', 'duration')
                          ]

