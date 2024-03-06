import threading
import sys
import time
import socket
import os

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

import twisted
from twisted.internet.task import LoopingCall
from twisted.internet import task
from twisted.internet.defer import inlineCallbacks, returnValue

from common.lib.clients.qtui.q_custom_text_changing_button import \
    TextChangingButton
from RF_gui import RFGui





SIGNALID1 = 445572


class RF_client(QWidget):

    def __init__(self, reactor, parent=None):
        super(RF_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()



    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'RF', password=self.password)
        self.rs =  self.cxn.rs_signal_generator
        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('Trap RF')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        gui = RFGui()


        
        init_freq = yield self.rs.get_frequency()
        gui.freq.setValue(init_freq)
        gui.freq.valueChanged.connect(lambda freq = gui.freq.value() \
                                                     : self.rfFreqChanged(freq))

        init_amp = yield self.rs.get_level()
        gui.amp.setValue(init_amp)
        gui.amp.valueChanged.connect(lambda amp = gui.amp.value() \
                                                 : self.rfAmpChanged(amp))


        init_state = yield self.rs.get_state()
        gui.on_switch.setChecked(init_state)
        gui.on_switch.toggled.connect(lambda state = gui.on_switch.isDown() \
                 : self.toggleRF(state))


        subLayout.addWidget(gui, 1, 1)
        self.setLayout(layout)
        self.show()

    @inlineCallbacks
    def rfFreqChanged(self, val):
        yield self.rs.set_frequency(val)
        
    @inlineCallbacks
    def rfAmpChanged(self, val):
        yield self.rs.set_level(val)

        
    @inlineCallbacks
    def toggleRF(self, state):
        yield self.rs.set_output(state)


        
if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = RF_client(reactor)
    client_inst.show()
    reactor.run()
