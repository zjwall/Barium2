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


class QCustomChannelSwitchGui(QFrame):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFrameStyle(0x0001 | 0x0030)
        self.makeLayout()

    def makeLayout(self):
        layout = QGridLayout()
        autoLayout = QGridLayout()
        
        shell_font = 'MS Shell Dlg 2'
        autoBox= QGroupBox("Automatic Switching:")
        manBox= QGroupBox("Manual Switching:")
        layout.addWidget
        title = QLabel('Fiber Switch Parameters')
        title.setFont(QFont(shell_font, pointSize=16))
        title.setAlignment(QtCore.Qt.AlignCenter)
    
        switchChannels = QLabel('Press to Enable Switching:')
        switchChannels.setFont(QFont(shell_font, pointSize=16))
        switchChannels.setAlignment(QtCore.Qt.AlignCenter)

        self.enableButton = TextChangingButton(('Enabled','Enable'))
        self.enableButton.setFont(QFont(shell_font, pointSize=16))
        self.enablelabel =  QLabel()
        self.enablelabel.setFont(QFont(shell_font, pointSize=16))
        self.enablelabel.setAlignment(QtCore.Qt.AlignCenter)
        
        switch_time = QLabel('Switch Time (ms)')
        switch_time.setFont(QFont(shell_font, pointSize=16))
        switch_time.setAlignment(QtCore.Qt.AlignCenter)


        # low rail
        self.switch_time = QDoubleSpinBox()
        self.switch_time.setFont(QFont(shell_font, pointSize=16))
        self.switch_time.setDecimals(0)
        self.switch_time.setSingleStep(1)
        self.switch_time.setRange(10 , 10000)
        self.switch_time.setKeyboardTracking(False)
        
        

        #layout 1 row at a time

        layout.addWidget(title,                    0, 2, 1, 4)

        layout.addWidget(switchChannels,           1, 0, 1, 4)

        layout.addWidget(self.enableButton,                  2, 1, 1, 1)
        

        layout.addWidget(switch_time,        2, 5, 1, 2)
        layout.addWidget(self.switch_time,      3, 5, 1, 2)
        
        


        layout.minimumSize()

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QCustomChannelSwitchGui()
    icon.show()
    app.exec_()

