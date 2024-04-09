
from barium.lib.scripts.pulse_sequences.pulse_sequence import pulse_sequence
from .DopplerCooling import DopplerCooling 
from .StateDetection import StateDetection 
from .Deshelving import Deshelving 


class ShelvingSub(pulse_sequence):

    required_parameters = [
                      ('ShelvingSub', 'duration')
                          ]

    required_subsequences = [DopplerCooling,StateDetection,Deshelving]
