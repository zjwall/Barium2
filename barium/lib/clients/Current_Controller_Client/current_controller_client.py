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
from current_controller_gui import CurrentGui


SIGNALID1 = 445572


class CurrentControllerClient(QWidget):

    def __init__(self, reactor, parent=None):
        super(CurrentControllerClient, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()


    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'CC Gui', password=self.password)
        self.cc = self.cxn.current_controller
        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):

        layout = QGridLayout()
        qBox = QGroupBox('Current Controller')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        gui = CurrentGui()

        init_amp = yield self.cc.get_current()
        gui.amp.setValue(init_amp)
        gui.amp.valueChanged.connect(lambda amp = gui.amp.value() \
                                                 : self.ccAmpChanged(amp))
        
        init_state = yield self.cc.get_output_state()
        gui.on_switch.setChecked(init_state)
        gui.on_switch.toggled.connect(lambda state = gui.on_switch.isDown() \
                 : self.change_output(state))
        
        subLayout.addWidget(gui, 1, 1)
        self.setLayout(layout)
        self.show()

    @inlineCallbacks
    def ccAmpChanged(self, val):
        yield self.cc.set_current(val)
        
    @inlineCallbacks
    def change_output(self, state):
        yield self.cc.set_output_state(state)
        





if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = CurrentControllerClient(reactor)
    client_inst.show()
    reactor.run()
