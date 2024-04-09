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
        autoBox= QGroupBox("Example")
        
        self.setLayout(layout)
        autoBox.setLayout(autoLayout)
        layout.addWidget(autoBox, 1,0)


        
    
        self.btn_start = QPushButton('Button')
        self.btn_start.resize(self.btn_start.sizeHint())
        self.btn_start.move(50, 50)



        



        #label for timing input box
        ch1_switch_time = QLabel('Entry Box')
        ch1_switch_time.setFont(QFont(shell_font, pointSize=16))
        ch1_switch_time.setAlignment(QtCore.Qt.AlignCenter)


        #box for timing input by user
        self.ch1_switch_time = QDoubleSpinBox()
        self.ch1_switch_time.setFont(QFont(shell_font, pointSize=16))
        self.ch1_switch_time.setDecimals(0)
        self.ch1_switch_time.setSingleStep(1)
        self.ch1_switch_time.setRange(100 , 10000)
        self.ch1_switch_time.setKeyboardTracking(False)







        autoLayout.addWidget(self.btn_start,                  2, 1, 1, 1)


        autoLayout.addWidget(ch1_switch_time,        1, 5, 1, 2)
        autoLayout.addWidget(self.ch1_switch_time,      2, 5, 1, 2)

        

        manLayout.minimumSize()
        autoLayout.minimumSize()
        
       


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QCustomFiberSwitchGui()
    icon.show()
    app.exec_()

