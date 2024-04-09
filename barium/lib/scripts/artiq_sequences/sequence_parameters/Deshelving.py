
from barium.lib.scripts.pulse_sequences.pulse_sequence import pulse_sequence


class Deshelving(pulse_sequence):

    required_parameters = [
                      ('Deshelving', 'duration')
                          ]

