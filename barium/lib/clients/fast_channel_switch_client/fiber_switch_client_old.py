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


from barium.lib.clients.gui.fiber_switch_gui import QCustomFiberSwitchGui

SIGNALID1 = 445567

class fiber_switch_client(QWidget):
    def __init__(self, reactor, parent=None):
        super(fiber_switch_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.channel = {}
        self.channel_GUIs = {}
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
        #self.set_up_channels()
        self.initializeGUI()
    


    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('Optical Fiber Switch')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
       
        
        yield self.reg.cd(['Clients','Fiber Switch Client'])
        self.channel_list = yield self.reg.get('Channels')
        

        print("a")
        self.channel = QCustomFiberSwitchGui()
        print("b")
        #init_chan = yield self.server.get_channel()
        print("c")
        #self.channel.displayChannel.setNum(int(init_chan))
        print("d")
            
        '''
        for now channels labels are stored in the registry as
        a list of 2-element arrays, i.e.,
        [['laser 1', channel num], ['laser 2', chan num], ...]
        stored in "registry/Clients/Fiber Switch Client"
        '''
        
        self.channel.c1.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[0][1]))
        self.channel.c2.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[1][1]))
        self.channel.c3.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[2][1]))
        self.channel.c4.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[3][1]))
        self.channel.c5.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[4][1]))
        self.channel.c6.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[5][1]))
        self.channel.c7.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[6][1]))
        self.channel.c8.clicked.connect(lambda:\
                    self.changeChannel(self.channel_list[7][1]))
            
        self.channel.checkChannel.clicked.connect(lambda: self.refreshNum())
    
        
#        print(channel1[0])
        self.channel.c1label.setText(str(self.channel_list[0][0]) + ' nm')
        self.channel.c2label.setText(str(self.channel_list[1][0]) + ' nm')
        self.channel.c3label.setText(str(self.channel_list[2][0]) + ' nm')
        self.channel.c4label.setText(str(self.channel_list[3][0]) + ' nm')
        self.channel.c5label.setText(str(self.channel_list[4][0]) + ' nm')
        self.channel.c6label.setText(str(self.channel_list[5][0]) + ' nm')
        self.channel.c7label.setText(str(self.channel_list[6][0]) + ' nm')
        self.channel.c8label.setText(str(self.channel_list[7][0]) + ' nm')
            

        #self.channel_GUIs[chan] = laser
        subLayout.addWidget(self.channel, 1, 1)
        layout.minimumSize()
        self.setLayout(layout)

    
    def changeNum(self, num):
        self.channel.displayChannel.setNum(int(num))
    
    @inlineCallbacks
    def changeChannel(self, num):
        yield self.server.set_channel(num)
        self.changeNum(int(num))
    
    @inlineCallbacks
    def refreshNum(self):
        num = yield self.server.get_channel()
        self.channel.displayChannel.setNum(int(num))
    


if __name__ == "__main__":
    a = QApplication( [] )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = fiber_switch_client(reactor)
    client_inst.show()
    reactor.run()
