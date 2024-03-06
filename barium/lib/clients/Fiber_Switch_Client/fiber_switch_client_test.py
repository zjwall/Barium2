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

SIGNALID1 = 445572

class fiber_switch_client(QWidget):
    #finished = pyqtSignal()
    #stop_signal = pyqtSignal()

    def __init__(self, reactor, parent=None):
        super(fiber_switch_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.channel = {}
        self.channel_GUIs = {}
        self.lasers={}
        #self.state = False
        self.run = True
        self.timer=1
        self.ch1_time=0
        self.ch2_time=0
        self.ch1="585nm" #ch1 laser name
        self.ch2="413nm" #ch2 laser name
        self.ch_list={}
        self.loop= 0
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
        self.lock_server = yield self.cxn.software_laser_lock_server
        #self.set_up_channels()
        #laser_lock = software_laser_lock_client(self.reactor)
##        yield self.reg.cd(['Servers','software_laser_lock'])
##        lasers_to_lock = yield self.reg.get('lasers')
##        for chan in lasers_to_lock:
##            self.lasers[chan] = yield self.reg.get(chan)
##            self.lasers[chan] = list(self.lasers[chan])
        self.initializeGUI()
    
    

    @inlineCallbacks
    def initializeGUI(self):
        print("initialize")
        layout = QGridLayout()
        qBox = QGroupBox('Optical Fiber Switch')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        
        yield self.reg.cd(['Clients','Fiber Switch Client'])
        self.channel_list = yield self.reg.get('Channels')
        self.channel = QCustomFiberSwitchGui()
        
        #init_chan = yield self.server.get_channel()
        #self.channel.displayChannel.setNum(int(init_chan))
            
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
            
        
        self.channel.c1label.setText(str(self.channel_list[0][0]) + ' nm')
        self.channel.c2label.setText(str(self.channel_list[1][0]) + ' nm')
        self.channel.c3label.setText(str(self.channel_list[2][0]) + ' nm')
        self.channel.c4label.setText(str(self.channel_list[3][0]) + ' nm')
        self.channel.c5label.setText(str(self.channel_list[4][0]) + ' nm')
        self.channel.c6label.setText(str(self.channel_list[5][0]) + ' nm')
        self.channel.c7label.setText(str(self.channel_list[6][0]) + ' nm')
        self.channel.c8label.setText(str(self.channel_list[7][0]) + ' nm')
            
        
        subLayout.addWidget(self.channel, 1, 1)
        layout.minimumSize()
        
        self.channel.btn_start.clicked.connect(self.set_switch)

        self.channel.btn_stop.clicked.connect(self.stop)
        self.setLayout(layout)
        self.show()
##        self.auto_lock()

    @inlineCallbacks
    def changeNum(self, num):
        yield self.channel.displayChannel.setNum(int(num))
    
    @inlineCallbacks
    def changeChannel(self, num):
        yield self.server.set_channel(num)
        self.changeNum(int(num))
    
    def changeChannel_nondefer(self, num):
        self.server.set_channel(num)
        self.changeNum(int(num))
        print("ended here")
    
    @inlineCallbacks
    def refreshNum(self):
        num = yield self.server.get_channel()
        self.channel.displayChannel.setNum(int(num))
    def set_switch(self):
        self.run=  True
        print(self.channel_list[1][1])
        self.lock_loop()
    def lock_loop(self):
       #self.reactor.callLater(self.timer, self.lock_loop)
       self.auto_lock()
    def auto_lock(self):
        if self.run:
            self.ch1_time= self.channel.ch1_switch_time.value()#read ch1 time box on gui as variable
            self.ch2_time= self.channel.ch2_switch_time.value()#read ch1 time box on gui as variable
            self.ch_list=[[self.ch1,self.ch1_time],[self.ch2,self.ch2_time]]
            self.lock_0(self.ch_list)

    def fuck_lock_step(self,ch_list,i):
        self.reactor.callLater(self.timer,self.lock_step_general(ch_list,(i)))
    
    def lock_0(self,ch_list):
        i=0
        self.changeChannel(self.channel_list[i][1])
        print(ch_list[i][1])
        #self.lock_server.lock_channel(True,ch_list[i][0])
        self.reactor.callLater(1,self.lock_step_general,ch_list=self.ch_list,i=((i+1)%len(self.ch_list)))
    
    def lock_step_general(self,ch_list,i):
        #self.lock_server.lock_channel(False,ch_list[(i+n-1)%len.(ch_list)])
        print(i)
        self.changeChannel(self.channel_list[i][1])
        print("channel changed")
        #self.lock_server.lock_channel(True,ch_list[i][0])
        self.loop=self.reactor.callLater(self.ch_list[i][1]/1000.0,self.lock_step_general,ch_list= self.ch_list,i=((i+1)%len(self.ch_list)))
        
    def stop(self):
        if self.run:
            self.loop.cancel()
        self.run= False
        print("stop worked")
        
       

if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = fiber_switch_client(reactor)
    client_inst.show()
    reactor.run()
