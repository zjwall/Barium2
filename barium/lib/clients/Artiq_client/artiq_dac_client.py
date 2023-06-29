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
from DAC_gui import DACGui





SIGNALID1 = 445572


class DAC_client(QWidget):

    def __init__(self, reactor, parent=None):
        super(DAC_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()



    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'DAC GUI', password=self.password)
        self.artiq =  self.cxn.artiq_server
        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('ARTIQ DAC')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        gui = DACGui()



        for i in range(32):
            init_volt = yield self.artiq.get_dac_val(i)
            gui.channels[i].dac.setValue(init_volt)
            gui.channels[i].dac.valueChanged.connect(lambda voltage = gui.channels[i].dac.value(), \
                                                     chan = i : self.dacChanged(chan,voltage))

        for i in range(32):
            init_state = yield self.artiq.get_dac_state(i)
            gui.channels[i].on_switch.setChecked(init_state)
            gui.channels[i].on_switch.toggled.connect(lambda state = gui.channels[i].on_switch.isDown(), chan = i \
                        : self.toggleDac(chan, state))

        subLayout.addWidget(gui, 1, 1)
        self.setLayout(layout)
        self.show()

    @inlineCallbacks
    def dacChanged(self, chan, val):
        yield self.artiq.set_dac(chan, val)

    @inlineCallbacks
    def toggleDac(self, chan, state):
        yield self.artiq.set_dac_state(chan, state)


        
if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = DAC_client(reactor)
    client_inst.show()
    reactor.run()
