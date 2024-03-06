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
from TTL_gui import TTLGui





SIGNALID1 = 445573


class TTL_client(QWidget):

    def __init__(self, reactor, parent=None):
        super(TTL_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()



    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'TTL GUI', password=self.password)
        self.artiq =  self.cxn.artiq_server
        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('ARTIQ TTL')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        gui = TTLGui()


        for i in range(20):
            init_state = yield self.artiq.get_ttl_state(i+4)
            gui.channels[i].on_switch.setChecked(init_state)
            gui.channels[i].on_switch.toggled.connect(lambda state = gui.channels[i].on_switch.isDown(), chan = i+4\
                        : self.toggleTTL(chan, state))


        
        subLayout.addWidget(gui, 1, 1)
        self.setLayout(layout)
##        self.show()


    @inlineCallbacks
    def toggleTTL(self, chan, state):
        yield self.artiq.set_ttl(chan, state)


        
if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = TTL_client(reactor)
    client_inst.show()
    reactor.run()
