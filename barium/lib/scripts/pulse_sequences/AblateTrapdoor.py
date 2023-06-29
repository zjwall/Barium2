from common.lib.servers.Pulser2.pulse_sequences.pulse_sequence import pulse_sequence
from sub_sequences.TrapLoad import trap_load
from labrad.units import WithUnit



class ablate_trapdoor(pulse_sequence):

    required_parameters = []

    required_subsequences = [trap_load]

    def sequence(self):
        self.addSequence(trap_load)




