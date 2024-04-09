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
from windfreak_gui import WindFreakGui





SIGNALID1 = 445572


class WindFreak_client(QWidget):

    def __init__(self, reactor, parent=None):
        super(WindFreak_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()



    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'WindFreak', password=self.password)
        self.wf =  self.cxn.wind
        self.setup()
        self.initializeGUI()

        
    @inlineCallbacks
    def setup(self):
        yield wf.set_reference()
        yield wf.set_reference_freq()
        
    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('1762 Windfreak')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        gui = WindFreakGui()


        
        init_freq = yield self.wf.read_freq()
        gui.freq.setValue(float(init_freq))
        gui.freq.valueChanged.connect(lambda freq = gui.freq.value() \
                                                     : self.wfFreqChanged(freq))

        init_amp = yield self.wf.read_power()
        gui.amp.setValue(float(init_amp))
        gui.amp.valueChanged.connect(lambda amp = gui.amp.value() \
                                                 : self.wfAmpChanged(amp))


        init_state = yield self.wf.read_output()
        gui.on_switch.setChecked(bool(int(init_state)))
        gui.on_switch.toggled.connect(lambda state = gui.on_switch.isDown() \
                 : self.toggleRF(state))


        subLayout.addWidget(gui, 1, 1)
        self.setLayout(layout)
        self.show()

    @inlineCallbacks
    def wfFreqChanged(self, val):
        yield self.wf.set_freq(val)
        
    @inlineCallbacks
    def wfAmpChanged(self, val):
        yield self.wf.set_power(val)

        
    @inlineCallbacks
    def toggleRF(self, state):
        yield self.wf.set_output(state)


        
if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = WindFreak_client(reactor)
    client_inst.show()
    reactor.run()
