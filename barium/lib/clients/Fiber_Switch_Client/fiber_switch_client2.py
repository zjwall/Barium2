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

from config.multiplexerclient_config2 import multiplexer_config
from common.lib.clients.qtui.q_custom_text_changing_button import \
    TextChangingButton
from barium.lib.clients.gui.software_laser_lock_gui import software_laser_lock_channel
#import barium.lib.clients.Software_Laser_Lock_Client.software_laser_lock_client #import software_laser_lock_client

from barium.lib.clients.gui.fiber_switch_gui import QCustomFiberSwitchGui

SIGNALID1 = 445572

class fiber_switch_client2(QWidget):
    #finished = pyqtSignal()
    #stop_signal = pyqtSignal()

    def __init__(self, reactor, parent=None):
        super(fiber_switch_client2, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.channel = {}
        self.channel_GUIs = {}
        self.lasers={}
        self.run = False
        self.fiber_switch_channel = 2
        self.timer=1
        self.ch_list=[['493nm',0,0],[0,0,0],['450nm',0,0],['413nm',0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
        self.loop= 0
        self.connect()

    @inlineCallbacks
    def connect(self):
        """Creates an Asynchronous connection to the wavemeter computer and
        connects incoming signals to relavent functions (((which computer???)))
        """
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']

        self.wm_cxn = yield connectAsync('10.97.109.81', name = \
                                      'Fiber Switch GUI', password=self.password)
        self.wm = yield self.wm_cxn.multiplexerserver

        self.cxn = yield connectAsync('localhost', name = \
                                      'Fiber Switch GUI', password=self.password)
        self.reg =  self.cxn.registry
        self.server =  self.cxn.fiber_switch_server2
        self.lock_server = yield self.cxn.software_laser_lock_server2

        yield self.reg.cd(['Servers','software_laser_lock'])
        lasers_to_lock = yield self.reg.get('lasers')
        for chan in lasers_to_lock:
            self.lasers[chan] = yield self.reg.get(chan)
            self.lasers[chan] = list(self.lasers[chan])

        self.initializeGUI()
        self.read_times()
        self.server.set_channel(1)

    #@inlineCallbacks this causes an error but no actual problems
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('Optical Fiber Switch')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        
        self.channel = QCustomFiberSwitchGui()
        
        self.channel.displayChannel.setNum(1)
        
        self.channel.btn_start.clicked.connect(self.set_switch)
        self.channel.btn_stop.clicked.connect(self.stop)

        self.channel.c1.clicked.connect(lambda:\
                    self.changeChannel(1))
        self.channel.c2.clicked.connect(lambda:\
                    self.changeChannel(2))
        self.channel.c3.clicked.connect(lambda:\
                    self.changeChannel(3))
        self.channel.c4.clicked.connect(lambda:\
                    self.changeChannel(4))
        self.channel.c5.clicked.connect(lambda:\
                    self.changeChannel(5))
        self.channel.c6.clicked.connect(lambda:\
                    self.changeChannel(6))
        self.channel.c7.clicked.connect(lambda:\
                    self.changeChannel(7))
        self.channel.c8.clicked.connect(lambda:\
                    self.changeChannel(8))
        
        self.channel.ch1_on.stateChanged.connect(lambda:\
                    self.update_check(0, self.channel.ch1_on))
        self.channel.ch2_on.stateChanged.connect(lambda:\
                    self.update_check(1, self.channel.ch2_on))
        self.channel.ch3_on.stateChanged.connect(lambda:\
                    self.update_check(2, self.channel.ch3_on))
        self.channel.ch4_on.stateChanged.connect(lambda:\
                    self.update_check(3, self.channel.ch4_on))
        self.channel.ch5_on.stateChanged.connect(lambda:\
                    self.update_check(4, self.channel.ch5_on))
        self.channel.ch6_on.stateChanged.connect(lambda:\
                    self.update_check(5, self.channel.ch6_on))
        self.channel.ch7_on.stateChanged.connect(lambda:\
                    self.update_check(6, self.channel.ch7_on))
        self.channel.ch8_on.stateChanged.connect(lambda:\
                    self.update_check(7, self.channel.ch8_on))

        self.set_labels()

        subLayout.addWidget(self.channel, 1, 1)
        layout.minimumSize()
        
        self.setLayout(layout)
        self.show()

    @inlineCallbacks
    def changeNum(self, num):
        yield self.channel.displayChannel.setNum(int(num))
    
    @inlineCallbacks
    def changeChannel(self, num):
        yield self.server.set_channel(num)
        self.changeNum(int(num))
        #print('set number to ' + str(num))
        '''
        use this code to have the laser on each channel automatically updated
        it's a little slow so easier to just manually update the label at the top in ch_list
        '''
        #if not self.run:
            #self.reactor.callLater(3, self.update_channel, i = num-1)
    
    def changeChannel_nondefer(self, num):
        self.server.set_channel(num)
        self.changeNum(int(num))
    
    @inlineCallbacks
    def refreshNum(self):
        num = yield self.server.get_channel()
        self.channel.displayChannel.setNum(int(num))

    def update_check(self, i, button):
        if button.isChecked():
            self.ch_list[i][2] = True
        else:
            self.ch_list[i][2] = False

    def set_switch(self):
        self.run=  True
        i = self.find_next(0)
        self.lock_loop(i)
    
    def lock_loop(self, i):
        if self.run:
            if self.ch_list[i][2]:
                self.read_times()
                #print((time.time()%1)*1000)
                #print('switch channel to ' + str(i+1))
                self.changeChannel(i+1)
                next_chan = self.find_next(i)
                self.loop = self.reactor.callLater(self.ch_list[i][1] / 1000., self.lock_loop, i = next_chan)
            else: # this is just in case someone has unchecked the channel after the loop for it was already created
                next_chan = self.find_next(i)
                self.lock_loop(next_chan)

    def find_next(self, i):
        for j in range(8):
            if self.ch_list[(i+j+1)%8][2]:
                return (i+j+1)%8
        self.run = False
        return 0

    def set_labels(self):
        self.channel.c1label.setText(str(self.ch_list[0][0]))
        self.channel.c2label.setText(str(self.ch_list[1][0]))
        self.channel.c3label.setText(str(self.ch_list[2][0]))
        self.channel.c4label.setText(str(self.ch_list[3][0]))
        self.channel.c5label.setText(str(self.ch_list[4][0]))
        self.channel.c6label.setText(str(self.ch_list[5][0]))
        self.channel.c7label.setText(str(self.ch_list[6][0]))
        self.channel.c8label.setText(str(self.ch_list[7][0]))

    @inlineCallbacks
    def update_channel(self, i):
        freq = yield self.wm.get_frequency(self.fiber_switch_channel)
        for laser in self.lasers:
            if abs(self.lasers[laser][0] - freq) < 10:
                self.ch_list[i][0] = laser
                break
        self.set_labels()

    def read_times(self):
        self.ch_list[0][1] = self.channel.ch1_switch_time.value()
        self.ch_list[1][1] = self.channel.ch2_switch_time.value()
        self.ch_list[2][1] = self.channel.ch3_switch_time.value()
        self.ch_list[3][1] = self.channel.ch4_switch_time.value()
        self.ch_list[4][1] = self.channel.ch5_switch_time.value()
        self.ch_list[5][1] = self.channel.ch6_switch_time.value()
        self.ch_list[6][1] = self.channel.ch7_switch_time.value()
        self.ch_list[7][1] = self.channel.ch8_switch_time.value()

    def stop(self):
        if self.run and self.loop != 0:
            self.loop.cancel()
        self.run= False
       

if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = fiber_switch_client2(reactor)
    client_inst.show()
    reactor.run()
