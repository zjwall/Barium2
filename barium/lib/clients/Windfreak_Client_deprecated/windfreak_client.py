from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from twisted.internet.defer import inlineCallbacks, returnValue
import socket
import os
from barium.lib.clients.gui.Windfreak_gui import QCustomWindfreakGui

class windfreak_client(QWidget):
    def __init__(self, reactor, parent=None):
        super(windfreak_client, self).__init__()
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
        self.cxn = yield connectAsync('localhost', name = socket.gethostname()\
                            + 'Windfreak GUI', password=self.password)
        #self.reg = self.cxn.registry
        self.server = self.cxn.windfreak
        #self.set_up_channels()
        self.initializeGUI()


    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('Windfreak')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue

        self.gui = QCustomWindfreakGui()
        init_freq = yield self.server.get_frequency()
        init_power = yield self.server.get_power()#power
        init_chan = yield self.server.get_channel()#channel
        init_onoff = yield self.server.get_onoff()#onoff
        self.gui.freqInput.setText(str(init_freq))#int(init_freq))
        self.gui.powerInput.setText(str(init_power))
        self.gui.chanNotif.setText(str(init_chan))
        self.gui.onoffNotif.setText(str(init_onoff))

        
        self.gui.c2.clicked.connect(lambda:\
                    self.changeFreq(self.gui.freqInput.text()))
        self.gui.c3.clicked.connect(lambda:\
                    self.changePower(self.gui.powerInput.text()))
        self.gui.c4.clicked.connect(lambda:\
                    self.on())
        self.gui.c5.clicked.connect(lambda:\
                    self.off())
        self.gui.c6.clicked.connect(lambda:\
                    self.changeChannel(0))
        self.gui.c7.clicked.connect(lambda:\
                    self.changeChannel(1))

        print('connected')
            
        #self.channel_GUIs[chan] = laser
        subLayout.addWidget(self.gui, 1, 1)
        layout.minimumSize()
        self.setLayout(layout)


    @inlineCallbacks
    def changeChannel(self, num):
        if num == 0:
            self.gui.chanNotif.setText('A')
        else:
            self.gui.chanNotif.setText('B')
        yield self.server.set_channel(num)
        self.changeONOFF()

    def changeONOFF(self):
        self.gui.onoffNotif.setText('?')

            
    @inlineCallbacks
    def changeFreq(self, num):
        yield self.server.set_freq(num)
        #self.changeNum(int(num))

    @inlineCallbacks
    def changePower(self, num):
        yield self.server.set_power(num)
        #self.changeNum(int(num))

    @inlineCallbacks
    def on(self):
        yield self.server.set_rf_on()
        self.set_text_on()

    def set_text_on(self):
        self.gui.onoffNotif.setText('ON')
        
    @inlineCallbacks
    def off(self):
        yield self.server.set_rf_off()
        self.set_text_off()

    def set_text_off(self):
        self.gui.onoffNotif.setText('OFF')        

if __name__ == "__main__":
    a = QApplication( [] )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = windfreak_client(reactor)
    client_inst.show()
    reactor.run()
