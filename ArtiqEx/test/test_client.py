from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
import threading
import sys
import time
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from twisted.internet.defer import inlineCallbacks, returnValue
import socket
import os
import twisted
from twisted.internet.task import LoopingCall
from twisted.internet import task

from config.multiplexerclient_config import multiplexer_config
from common.lib.clients.qtui.q_custom_text_changing_button import \
    TextChangingButton
from barium.lib.clients.gui.software_laser_lock_gui import software_laser_lock_channel
#import barium.lib.clients.Software_Laser_Lock_Client.software_laser_lock_client #import software_laser_lock_client

from barium.lib.clients.gui.fiber_switch_gui import QCustomFiberSwitchGui
from DAC_gui import DACGui

SIGNALID1 = 445572

class fiber_switch_client(QWidget):
    
    def __init__(self, reactor, parent=None):
        super(fiber_switch_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.channel = {}

        self.connect()

    @inlineCallbacks
    def connect(self):
        """Creates an Asynchronous connection to the wavemeter computer and
        connects incoming signals to relavent functions (((which computer???)))
        """
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'Fiber Switch GUI', password=self.password)
        self.reg =  self.cxn.registry
        self.server =  self.cxn.fiber_switch_server

        self.initializeGUI()
    
    

    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('Optical Fiber Switch')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        

        self.channel = DACGui()


            
        
        subLayout.addWidget(self.channel, 1, 1)

        self.setLayout(layout)
        self.show()

       

if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = fiber_switch_client(reactor)
    client_inst.show()
    reactor.run()
