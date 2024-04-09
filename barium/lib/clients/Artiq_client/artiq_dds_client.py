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
from DDS_gui import DDSGui
from barium.lib.servers.Artiq.artiq_config import config





SIGNALID1 = 445572


class DDS_client(QWidget):

    def __init__(self, reactor, parent=None):
        super(DDS_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()



    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'DDS GUI', password=self.password)
        self.artiq =  self.cxn.artiq_server
        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('ARTIQ DDS')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        gui = DDSGui()


        self.dds_list = yield self.artiq.list_dds()
        
        for i in range(12):

            if i in config.DDS_dict.keys():
                init_freq = config.DDS_dict[i][1]
            else:
                init_freq = yield self.artiq.get_dds_freq(self.dds_list[i])
            gui.channels[i].freq.setValue(init_freq)
            gui.channels[i].freq.valueChanged.connect(lambda freq = gui.channels[i].freq.value(), \
                                                     chan = self.dds_list[i] : self.ddsFreqChanged(chan,freq))

        for i in range(12):
            if i in config.DDS_dict.keys():
                init_amp = config.DDS_dict[i][2]
            else:
                init_amp = yield self.artiq.get_dds_amp(self.dds_list[i])
            gui.channels[i].amp.setValue(init_amp)
            gui.channels[i].amp.valueChanged.connect(lambda amp = gui.channels[i].amp.value(), \
                                                     chan = self.dds_list[i] : self.ddsAmpChanged(chan,amp))

        for i in range(12):
            if i in config.DDS_dict.keys():
                init_att = config.DDS_dict[i][3]
            else:
                init_att = yield self.artiq.get_dds_att(self.dds_list[i])
            gui.channels[i].att.setValue(init_att)
            gui.channels[i].att.valueChanged.connect(lambda att = gui.channels[i].att.value(), \
                                                     chan = self.dds_list[i] : self.ddsAttChanged(chan,att))    

        for i in range(12):
            if i in config.DDS_dict.keys():
                init_state = config.DDS_dict[i][4]
            else:
                init_state = yield self.artiq.get_dds_state(self.dds_list[i])
            gui.channels[i].on_switch.setChecked(init_state)
            gui.channels[i].on_switch.toggled.connect(lambda state = gui.channels[i].on_switch.isDown(), chan = self.dds_list[i] \
                        : self.toggleDDS(chan, state))


        subLayout.addWidget(gui, 1, 1)
        self.setLayout(layout)
##        self.show()

    @inlineCallbacks
    def ddsFreqChanged(self, chan, val):
        yield self.artiq.set_dds_freq(chan, val)
        
    @inlineCallbacks
    def ddsAmpChanged(self, chan, val):
        yield self.artiq.set_dds_amp(chan, val)

    @inlineCallbacks
    def ddsAttChanged(self, chan, val):
        yield self.artiq.set_dds_att(chan, val)
        
    @inlineCallbacks
    def toggleDDS(self, chan, state):
        yield self.artiq.toggle_dds(chan, state)


        
if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = DDS_client(reactor)
    client_inst.show()
    reactor.run()
