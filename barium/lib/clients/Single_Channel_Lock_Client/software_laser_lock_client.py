#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PyQt4 import QtGui, QtCore
from twisted.internet.defer import inlineCallbacks, returnValue
import socket
import os
from config.multiplexerclient_config import multiplexer_config
from common.lib.clients.qtui.q_custom_text_changing_button import \
    TextChangingButton
from barium.lib.clients.gui.software_laser_lock_gui import software_laser_lock_channel

SIGNALID1 = 445567


class software_laser_lock_client(QtGui.QWidget):
    def __init__(self, reactor, parent=None):
        super(software_laser_lock_client, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.reactor = reactor
        self.lasers = {}
        self.channel_GUIs = {}
        self.connect()

    @inlineCallbacks
    def connect(self):
        """Creates an Asynchronous connection to the wavemeter computer and
        connects incoming signals to relavent functions
        """
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.wm_cxn = yield connectAsync(multiplexer_config.ip, name = socket.gethostname() + ' Single Channel Lock', password=self.password)
        self.wm = yield self.wm_cxn.multiplexerserver
        self.cxn = yield connectAsync('bender', name = socket.gethostname() + ' Single Channel Lock', password=self.password)
        self.lock_server = yield self.cxn.software_laser_lock_server
        self.registry = self.cxn.registry

        # Get lasers to lock
        yield self.registry.cd(['Servers','software_laser_lock'])
        lasers_to_lock = yield self.registry.get('lasers')
        for chan in lasers_to_lock:
            self.lasers[chan] = yield self.registry.get(chan)

        yield self.wm.signal__frequency_changed(SIGNALID1)
        yield self.wm.addListener(listener = self.updateFrequency, source = None, ID = SIGNALID1)

        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):
        layout = QtGui.QGridLayout()
        qBox = QtGui.QGroupBox('Single Channel Software Lock')
        subLayout = QtGui.QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue

        for chan in self.lasers:
            laser = software_laser_lock_channel(chan)

            init_freq1 = yield self.lock_server.get_lock_frequency(chan)
            laser.spinFreq1.setValue(init_freq1)
            laser.spinFreq1.valueChanged.connect(lambda freq = laser.spinFreq1.value(), chan = chan \
                                            : self.freqChanged(freq, chan))

            state = yield self.lock_server.get_lock_state(chan)
            laser.lockSwitch.setChecked(state)
            laser.lockSwitch.toggled.connect(lambda state = laser.lockSwitch.isDown(), chan = chan  \
                                             : self.set_lock(state, chan))


            init_exp = yield self.wm.get_exposure(self.lasers[chan][0])
            laser.spinExposure.setValue(init_exp)
            laser.spinExposure.valueChanged.connect(lambda exp = laser.spinExposure.value(), \
                                            chan = chan, : self.expChanged(exp, chan))

            init_gain = yield self.lock_server.get_gain(chan)
            laser.spinGain.setValue(init_gain)
            laser.spinGain.valueChanged.connect(lambda gain = laser.spinGain.value(), \
                                            chan = chan : self.gainChanged(gain, chan))


            init_rails = yield self.lock_server.get_rails(chan)
            laser.spinLowRail.setValue(init_rails[0])
            laser.spinLowRail.valueChanged.connect(lambda rail = laser.spinLowRail.value(), \
                                                   chan = chan  : self.lowRailChanged(rail, chan))

            laser.spinHighRail.setValue(init_rails[1])
            laser.spinHighRail.valueChanged.connect(lambda rail = laser.spinHighRail.value(), \
                                                    chan = chan : self.highRailChanged(rail, chan))

            laser.clear_lock.clicked.connect(lambda : self.reset_lock(chan))

            self.channel_GUIs[chan] = laser
            subLayout.addWidget(laser, self.lasers[chan][2][0], self.lasers[chan][2][1] , 1, 1)
            self.setLayout(layout)


    @inlineCallbacks
    def freqChanged(self, freq, chan):
        yield self.lock_server.set_lock_frequency(freq, chan)

    @inlineCallbacks
    def expChanged(self, exp, chan):
        yield self.wm.set_exposure_time(self.lasers[chan][0],int(exp))

    @inlineCallbacks
    def gainChanged(self, gain, chan):
        yield self.lock_server.set_gain(gain, chan)

    @inlineCallbacks
    def lowRailChanged(self, value, chan):
        yield self.lock_server.set_low_rail(value, chan)


    @inlineCallbacks
    def highRailChanged(self, value, chan):
        yield self.lock_server.set_high_rail(value, chan)

    @inlineCallbacks
    def updateFrequency(self, c, signal):
        for chan in self.lasers:
            if signal[0] == self.lasers[chan][0]:

                laser = self.channel_GUIs[chan]
                laser.wavelength.setText('{:.6f}'.format(signal[1]))
                voltage = yield self.lock_server.get_dac_voltage(chan)
                laser.dacVoltage.setText('{:.3f}'.format(voltage))

    @inlineCallbacks
    def set_lock(self, state, chan):
        yield self.lock_server.lock_channel(state, chan)

    @inlineCallbacks
    def reset_lock(self, chan):
        yield self.lock_server.reset_lock(chan)


if __name__ == "__main__":
    a = QtGui.QApplication( [] )
    import qt4reactor
    qt4reactor.install()
    from twisted.internet import reactor
    software_lock = software_laser_lock_client(reactor)
    software_lock.show()
    reactor.run()
