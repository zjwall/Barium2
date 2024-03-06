import threading
import sys
import time
import socket
import os
import numpy as np 
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
from PMT_gui import PMTGui


class PMT_client(QWidget):

    name = 'PMT Client'

    def __init__(self, reactor, parent=None):
        super(PMT_client, self).__init__()
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.reactor = reactor
        self.connect()

    @inlineCallbacks
    def connect(self):
        from labrad.wrappers import connectAsync
        self.password = os.environ['LABRADPASSWORD']
        self.cxn = yield connectAsync('localhost', name = \
                                      'PMT GUI', password=self.password)
        self.artiq =  self.cxn.artiq_server
        self.dv = self.cxn.data_vault
        ##claxton
        self.c_record = self.cxn.context()
        self.recording = False
        self.starttime = 0
        # create polling loop
        self.refresher = LoopingCall(self.update_counts)
        self._sample_time_us = 0
        self._num_samples = 0
        self._time_per_data = 0
##        ##
        self.initializeGUI()

    @inlineCallbacks
    def initializeGUI(self):
        layout = QGridLayout()
        qBox = QGroupBox('PMT')
        subLayout = QGridLayout()
        qBox.setLayout(subLayout)
        layout.addWidget(qBox, 0, 0), returnValue
        self.gui = PMTGui()

        self.gui.count_display.display("OFF")
        init_state = False
        self.gui.on_switch.setChecked(init_state)
        self.gui.on_switch.toggled.connect(lambda status: self.toggle_polling(status))

        subLayout.addWidget(self.gui, 1, 1)
        self.setLayout(layout)
        self.show()

        
    @inlineCallbacks
    def update_counts(self):
        """
        Main function that actually gets counts from artiq.
        """
        # get counts
        count_list = yield self.artiq.ttl_count_list(0, self.sample_time_us, self.num_samples)

        # update display
        self.gui.count_display.setFont(QFont('MS Shell Dlg 2', pointSize=19))
        self.gui.count_display.display(np.mean(count_list))
        print(np.mean(count_list))
        # store data if recording
        if self.recording:
            yield self.dv.add(time() - self.starttime, np.mean(count_list), context=self.c_record)

    def toggle_polling(self, status):
        print('hi')
        if status and (not self.refresher.running):
            # get timing values
            poll_interval_s = 1
            self.sample_time_us = int(100000)
            self.num_samples = int(1)
            time_per_data = self.sample_time_us * self.num_samples * 1e-6
            # ensure valid timing
            if (time_per_data > poll_interval_s) or (time_per_data > 1):
                raise Exception("Error: invalid timing.")
            # set up display and start polling
            self.refresher.start(poll_interval_s, now=True)
        # stop if running
        elif (not status) and (self.refresher.running):
            self.refresher.stop()
            self.gui.count_display.display("OFF")

        


##    @inlineCallbacks
##    def record(self, status):
##        """
##        Creates a new dataset to record counts
##        tells polling loop to add data to data vault.
##        """
##        self.recording = status
##        # set up datavault
##        if self.recording:
##            self.starttime = time()
##            trunk = createTrunk(self.name)
##            yield self.dv.cd(trunk, True, context=self.c_record)
##            yield self.dv.new('PMT', [('Elapsed time', 't')], [('PMT Counts', 'Counts', 'Number')], context=self.c_record)
##





if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = PMT_client(reactor)
    client_inst.show()
    reactor.run()
