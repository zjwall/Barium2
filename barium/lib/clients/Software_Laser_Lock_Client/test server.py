#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from twisted.internet.defer import inlineCallbacks, returnValue
import socket
import os
import twisted
from config.multiplexerclient_config import multiplexer_config
from common.lib.clients.qtui.q_custom_text_changing_button import \
    TextChangingButton
from barium.lib.clients.gui.software_laser_lock_gui import software_laser_lock_channel


SIGNALID1 = 445567
SIGNALID2 = 445568
SIGNALID3 = 445569
SIGNALID4 = 445570


class software_laser_lock_client(QWidget):
    def __init__(self, parent=None):
        super(software_laser_lock_client, self).__init__()
        #self.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        #self.reactor = reactor
        self.lasers = {}
        self.channel_GUIs = {}
        self.connect()

    def connect(self):
##        """Creates an Asynchronous connection to the wavemeter computer and
##        connects incoming signals to relavent functions
##        """
        from labrad.__init__ import connect
        self.password = os.environ['LABRADPASSWORD']
        self.wm_cxn = yield connectAsync(multiplexer_config.ip, name = socket.gethostname() + ' Single Channel Lock', password=self.password)
        self.wm = yield self.wm_cxn.multiplexerserver
        #self.cxn = yield connectAsync('localhost', name = socket.gethostname() + ' Single Channel Lock', password=self.password)
        self.cxn = yield connect('flexo', name = socket.gethostname() + ' Single Channel Lock', password=self.password)
        #self.lock_server = connectAsync('localhost', name = socket.gethostname() + ' Single Channel Lock', password=self.password)#= yield self.cxn.software_laser_lock_server
        self.lock_server = self.cxn.lock_server
        #self.bristol = yield self.cxn.bristolserver
        self.piezo = yield self.cxn.piezo_controller
        self.registry = self.cxn.registry

        

        # Get lasers to lock
        yield self.registry.cd(['Servers','software_laser_lock'])
        lasers_to_lock = yield self.registry.get('lasers')
        for chan in lasers_to_lock:
           self.lasers[chan] = yield self.registry.get(chan)

   
       
        

        self.initializeGUI()

    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('Single Channel Software Lock')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0)#, returnValue
        for chan in self.lasers:
##            laser = software_laser_lock_channel(chan)
##            from common.lib.clients.qtui import RGBconverter as RGB
##            RGB = RGB.RGBconverter()
##            color = int(2.998e8/(float(self.lasers[chan][0])*1e3))
##            color = RGB.wav2RGB(color)
##            color = tuple(color)
##            laser.wavelength.setStyleSheet('color: rgb' + str(color))
##            init_freq1 = yield self.lock_server.get_lock_frequency(chan)
##            laser.spinFreq1.setValue(init_freq1)
##            laser.spinFreq1.valueChanged.connect(lambda freq = laser.spinFreq1.value(), chan = chan \
##                                            : self.freqChanged(freq, chan))

##            state = yield self.lock_server.get_lock_state(chan)
##            laser.lockSwitch.setChecked(state)
##            laser.lockSwitch.toggled.connect(lambda state = laser.lockSwitch.isDown(), chan = chan  \
##                                             : self.set_lock(state, chan))
##
##
##            init_exp = yield self.wm.get_exposure(self.lasers[chan][1])
##            laser.spinExposure.setValue(init_exp)
##            laser.spinExposure.valueChanged.connect(lambda exp = laser.spinExposure.value(), \
##                                            chan = chan, : self.expChanged(exp, chan))
##
##            init_gain = yield self.lock_server.get_gain(chan)
##            laser.spinGain.setValue(init_gain)
##            laser.spinGain.valueChanged.connect(lambda gain = laser.spinGain.value(), \
##                                            chan = chan : self.gainChanged(gain, chan))
##
##
##            init_rails = yield self.lock_server.get_rails(chan)
##            laser.spinLowRail.setValue(init_rails[0])
##            laser.spinLowRail.valueChanged.connect(lambda rail = laser.spinLowRail.value(), \
##                                                   chan = chan  : self.lowRailChanged(rail, chan))
##
##            laser.spinHighRail.setValue(init_rails[1])
##            laser.spinHighRail.valueChanged.connect(lambda rail = laser.spinHighRail.value(), \
##                                                    chan = chan : self.highRailChanged(rail, chan))
##
##            laser.clear_lock.clicked.connect(lambda state = laser.clear_lock.isDown(), chan = chan : self.reset_lock(chan))
##
##            laser.spinDacVoltage.valueChanged.connect(lambda voltage = laser.spinDacVoltage.value(), \
##                                                    chan = chan : self.voltageChanged(voltage, chan))

            self.channel_GUIs[chan] = laser
            subLayout.addWidget(laser, self.lasers[chan][2][0], self.lasers[chan][2][1] , 1, 1)
            self.setLayout(layout)


if __name__ == "__main__":
    a = QApplication([])
##    import qt5reactor
##    qt5reactor.install()
##    from twisted.internet import reactor
    software_lock = software_laser_lock_client()
    
    software_lock.show()
    
    #reactor.run()
