# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 18:14:56 2020

@author: barium133
"""

import sys
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from common.lib.clients.qtui.q_custom_text_changing_button import \
    TextChangingButton as _TextChangingButton

class TextChangingButton(_TextChangingButton):
    def __init__(self, button_text=None, parent=None):
       super(TextChangingButton, self).__init__(button_text, parent)
       self.setMaximumHeight(30)

class StretchedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setMinimumSize(QtCore.QSize(500, 300))

    def resizeEvent(self, evt):

        font = self.font()
        font.setPixelSize(self.width() * 0.14 - 14)
        self.setFont(font)


class QCustomFiberSwitchGui(QFrame):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFrameStyle(0x0001 | 0x0030)
        self.makeLayout()

    def makeLayout(self):
        layout = QGridLayout()
        autoLayout = QGridLayout()
        manLayout = QGridLayout()
        
        shell_font = 'MS Shell Dlg 2'
        autoBox= QGroupBox("Automatic Switching:")
        manBox= QGroupBox("Manual Switching:")
        
        self.setLayout(layout)
        manBox.setLayout(manLayout)
        autoBox.setLayout(autoLayout)
        layout.addWidget(autoBox, 1,0)
        layout.addWidget(manBox,1,1)
        title = QLabel('Fiber Switch Parameters')
        title.setFont(QFont(shell_font, pointSize=16))
        title.setAlignment(QtCore.Qt.AlignCenter)

        switchChannels = QLabel('Press to Enable Switching:')
        switchChannels.setFont(QFont(shell_font, pointSize=16))
        switchChannels.setAlignment(QtCore.Qt.AlignCenter)
        
        #create button to enable automatic switching 
##        self.enableButton = TextChangingButton(('Enabled','nEnable'))
##        self.enableButton.setFont(QFont(shell_font, pointSize=16))
##        self.enablelabel =  QLabel()
##        self.enablelabel.setFont(QFont(shell_font, pointSize=16))
##        self.enablelabel.setAlignment(QtCore.Qt.AlignCenter)
##        

        self.btn_start = QPushButton('Start')
        self.btn_start.resize(self.btn_start.sizeHint())
        self.btn_start.move(50, 50)
        self.btn_stop = QPushButton('Stop')
        self.btn_stop.resize(self.btn_stop.sizeHint())
        self.btn_stop.move(150, 50)
        #Define all fiber channels 1-8
        self.c1 = QPushButton("1", self)
        self.c1. setFont(QFont(shell_font, pointSize=16))
        self.c1label =  QLabel()
        self.c1label.setFont(QFont(shell_font, pointSize=16))
        self.c1label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c2 = QPushButton("2", self)
        self.c2.setFont(QFont(shell_font, pointSize=16))
        self.c2label =  QLabel()
        self.c2label.setFont(QFont(shell_font, pointSize=16))
        self.c2label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c3 = QPushButton("3", self)
        self.c3.setFont(QFont(shell_font, pointSize=16))
        self.c3label =  QLabel()
        self.c3label.setFont(QFont(shell_font, pointSize=16))
        self.c3label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c4 = QPushButton("4", self)
        self.c4.setFont(QFont(shell_font, pointSize=16))
        self.c4label =  QLabel()
        self.c4label.setFont(QFont(shell_font, pointSize=16))
        self.c4label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c5 = QPushButton("5", self)
        self.c5.setFont(QFont(shell_font, pointSize=16))
        self.c5label =  QLabel()
        self.c5label.setFont(QFont(shell_font, pointSize=16))
        self.c5label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c6 = QPushButton("6", self)
        self.c6.setFont(QFont(shell_font, pointSize=16))
        self.c6label =  QLabel()
        self.c6label.setFont(QFont(shell_font, pointSize=16))
        self.c6label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c7 = QPushButton("7", self)
        self.c7.setFont(QFont(shell_font, pointSize=16))
        self.c7label =  QLabel()
        self.c7label.setFont(QFont(shell_font, pointSize=16))
        self.c7label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c8 = QPushButton("8", self)
        self.c8.setFont(QFont(shell_font, pointSize=16))
        self.c8label =  QLabel()
        self.c8label.setFont(QFont(shell_font, pointSize=16))
        self.c8label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.checkChannel = QLabel("Current Channel", self)
        self.checkChannel.setFont(QFont(shell_font, pointSize=16))
        
        self.displayChannel = QLabel('0') #not sure if this is how u do it
        self.displayChannel.setFont(QFont(shell_font, pointSize=16))
        self.displayChannel.setAlignment(QtCore.Qt.AlignCenter)

        #label for timing input box
        ch1_switch_time = QLabel('Ch 1 Wavemeter Time (ms)')
        ch1_switch_time.setFont(QFont(shell_font, pointSize=16))
        ch1_switch_time.setAlignment(QtCore.Qt.AlignCenter)


        #box for timing input by user
        self.ch1_switch_time = QDoubleSpinBox()
        self.ch1_switch_time.setFont(QFont(shell_font, pointSize=16))
        self.ch1_switch_time.setDecimals(0)
        self.ch1_switch_time.setSingleStep(1)
        self.ch1_switch_time.setRange(500 , 100000)
        self.ch1_switch_time.setKeyboardTracking(False)


        ch2_switch_time = QLabel('Ch 2 Wavemeter Time (ms)')
        ch2_switch_time.setFont(QFont(shell_font, pointSize=16))
        ch2_switch_time.setAlignment(QtCore.Qt.AlignCenter)


        #box for timing input by user
        self.ch2_switch_time = QDoubleSpinBox()
        self.ch2_switch_time.setFont(QFont(shell_font, pointSize=16))
        self.ch2_switch_time.setDecimals(0)
        self.ch2_switch_time.setSingleStep(1)
        self.ch2_switch_time.setRange(500 , 100000)
        self.ch2_switch_time.setKeyboardTracking(False)

        ch3_switch_time = QLabel('Ch 3 Wavemeter Time (ms)')
        ch3_switch_time.setFont(QFont(shell_font, pointSize=16))
        ch3_switch_time.setAlignment(QtCore.Qt.AlignCenter)


        #box for timing input by user
        self.ch3_switch_time = QDoubleSpinBox()
        self.ch3_switch_time.setFont(QFont(shell_font, pointSize=16))
        self.ch3_switch_time.setDecimals(0)
        self.ch3_switch_time.setSingleStep(1)
        self.ch3_switch_time.setRange(500 , 100000)
        self.ch3_switch_time.setKeyboardTracking(False)

        manLayout.addWidget(title,                    0, 2, 1, 4)

        manLayout.addWidget(switchChannels,           0, 0, 1, 4)

        manLayout.addWidget(self.c1,                  2, 0, 1, 1)
        manLayout.addWidget(self.c2,                  2, 1, 1, 1)
        manLayout.addWidget(self.c3,                  2, 2, 1, 1)
        manLayout.addWidget(self.c4,                  2, 3, 1, 1)

        manLayout.addWidget(self.c5,                  4, 0, 1, 1)
        manLayout.addWidget(self.c6,                  4, 1, 1, 1)
        manLayout.addWidget(self.c7,                  4, 2, 1, 1)
        manLayout.addWidget(self.c8,                  4, 3, 1, 1)

        manLayout.addWidget(self.checkChannel,        2, 5, 1, 2)
        manLayout.addWidget(self.displayChannel,      3, 5, 1, 2)
        
        manLayout.addWidget(self.c1label,                  3, 0, 1, 1)
        manLayout.addWidget(self.c2label,                  3, 1, 1, 1)
        manLayout.addWidget(self.c3label,                  3, 2, 1, 1)
        manLayout.addWidget(self.c4label,                  3, 3, 1, 1)

        manLayout.addWidget(self.c5label,                  5, 0, 1, 1)
        manLayout.addWidget(self.c6label,                  5, 1, 1, 1)
        manLayout.addWidget(self.c7label,                  5, 2, 1, 1)
        manLayout.addWidget(self.c8label,                  5, 3, 1, 1)
        autoLayout.addWidget(switchChannels,           0, 0, 1, 4)

        #autoLayout.addWidget(self.enableButton,                  2, 1, 1, 1)
        autoLayout.addWidget(self.btn_start,                  2, 1, 1, 1)
        autoLayout.addWidget(self.btn_stop,                  2, 2, 1, 1)


        autoLayout.addWidget(ch1_switch_time,        1, 5, 1, 2)
        autoLayout.addWidget(self.ch1_switch_time,      2, 5, 1, 2)
        autoLayout.addWidget(ch2_switch_time,        3, 5, 1, 2)
        autoLayout.addWidget(self.ch2_switch_time,      4, 5, 1, 2)
        autoLayout.addWidget(ch3_switch_time,        5, 5, 1, 2)
        autoLayout.addWidget(self.ch3_switch_time,      6, 5, 1, 2)

        manLayout.minimumSize()
        autoLayout.minimumSize()
        
       


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QCustomFiberSwitchGui()
    icon.show()
    app.exec_()

