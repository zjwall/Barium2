from common.lib.servers.Pulser2.pulse_sequences.pulse_sequence import pulse_sequence

"""

"""

class trap_load(pulse_sequence):

    required_parameters = [('Trapdoor', 'Trap_RF_TTL'),
                           ('Trapdoor', 'Flashlamp_TTL'),
                           ('Trapdoor', 'QSwitch_Delay'),
                           ('Trapdoor', 'Trap_Delay'), ]

    def sequence(self):
        # start time is defined to be 0s.
        p = self.parameters.Trapdoor

        self.rf_ttl = p.Trap_RF_TTL
        self.flash_ttl = p.Flashlamp_TTL
        self.t_qswitch = p.QSwitch_Delay
        self.trap_delay = p.Trap_Delay


        self.addTTL(self.rf_ttl, self.start, self.t_qswitch + self.trap_delay)
        self.addTTL(self.flash_ttl, self.start, self.t_qswitch + self.trap_delay)

        
        self.end = self.start + self.t_qswitch + self.trap_delay



