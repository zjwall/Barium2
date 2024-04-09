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
    TextChangingButton


class StretchedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setMinimumSize(QtCore.QSize(500, 300))

    def resizeEvent(self, evt):

        font = self.font()
        font.setPixelSize(self.width() * 0.14 - 14)
        self.setFont(font)


class QCustomWindfreakGui(QFrame):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFrameStyle(0x0001 | 0x0030)
        self.makeLayout()
        buttonStyleSheet = """
        color: white;
        background-color: {};
        """

    def action(self, button1, button2):
        """
        Create the effect of selected button1
        and unselect button2 or vice versa.
        """
        

    def makeLayout(self):
        layout = QGridLayout()

        shell_font = 'MS Shell Dlg 2'
        title = QLabel('Windfreak')
        title.setFont(QFont(shell_font, pointSize=16))
        title.setAlignment(QtCore.Qt.AlignCenter)

        freqText = QLabel('Frequency: ')
        freqText.setFont(QFont(shell_font, pointSize=16))
        freqText.setAlignment(QtCore.Qt.AlignCenter)

        self.freqInput = QLineEdit(self)
        self.freqInput.setFont(QFont(shell_font, pointSize=16))
        #self.c1label =  QLabel()
        #self.c1label.setFont(QFont(shell_font, pointSize=16))
        #self.c1label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c2 = QPushButton("confirm", self)
        self.c2.setFont(QFont(shell_font, pointSize=16))
        self.c2label =  QLabel()
        self.c2label.setFont(QFont(shell_font, pointSize=16))
        self.c2label.setAlignment(QtCore.Qt.AlignCenter)

        powerText = QLabel('Power: ')
        powerText.setFont(QFont(shell_font, pointSize=16))
        powerText.setAlignment(QtCore.Qt.AlignCenter)

        self.powerInput = QLineEdit(self)
        self.powerInput.setFont(QFont(shell_font, pointSize=16))
        #self.c1label =  QLabel()
        #self.c1label.setFont(QFont(shell_font, pointSize=16))
        #self.c1label.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c3 = QPushButton("confirm", self)
        self.c3.setFont(QFont(shell_font, pointSize=16))
        self.c3label =  QLabel()
        self.c3label.setFont(QFont(shell_font, pointSize=16))
        self.c3label.setAlignment(QtCore.Qt.AlignCenter)

        onoffText = QLabel('RF On/Off: ')
        onoffText.setFont(QFont(shell_font, pointSize=16))
        onoffText.setAlignment(QtCore.Qt.AlignCenter)

        self.onoffNotif = QLabel('ON')
        self.onoffNotif.setFont(QFont(shell_font, pointSize=16))
        self.onoffNotif.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c4 = QPushButton("ON", self)
        self.c4.setFont(QFont(shell_font, pointSize=16))
        self.c4label =  QLabel()
        self.c4label.setFont(QFont(shell_font, pointSize=16))
        self.c4label.setAlignment(QtCore.Qt.AlignCenter)
##        self.c4.setStyleSheet("QPushButton"
##                             "{"
##                             "background-color : lightblue;"
##                             "}"
##                             "QPushButton::pressed"
##                             "{"
##                             "background-color : red;"
##                             "}"
##                             )
        #self.c4.clicked.connect(self.action(4, 5))

        self.c5 = QPushButton("OFF", self)
        self.c5.setFont(QFont(shell_font, pointSize=16))
        self.c5label =  QLabel()
        self.c5label.setFont(QFont(shell_font, pointSize=16))
        self.c5label.setAlignment(QtCore.Qt.AlignCenter)
##        self.c5.setStyleSheet("QPushButton"
##                             "{"
##                             "background-color : lightblue;"
##                             "}"
##                             "QPushButton::pressed"
##                             "{"
##                             "background-color : red;"
##                             "}"
##                             )

        chanText = QLabel('Current Channel: ')
        chanText.setFont(QFont(shell_font, pointSize=16))
        chanText.setAlignment(QtCore.Qt.AlignCenter)

        self.chanNotif = QLabel('A')
        self.chanNotif.setFont(QFont(shell_font, pointSize=16))
        self.chanNotif.setAlignment(QtCore.Qt.AlignCenter)
        
        self.c6 = QPushButton("A", self)
        self.c6.setFont(QFont(shell_font, pointSize=16))
        self.c6label =  QLabel()
        self.c6label.setFont(QFont(shell_font, pointSize=16))
        self.c6label.setAlignment(QtCore.Qt.AlignCenter)
##        self.c6.setStyleSheet("QPushButton"
##                             "{"
##                             "background-color : lightblue;"
##                             "}"
##                             "QPushButton::pressed"
##                             "{"
##                             "background-color : red;"
##                             "}"
##                             )

        self.c7 = QPushButton("B", self)
        self.c7.setFont(QFont(shell_font, pointSize=16))
        self.c7label =  QLabel()
        self.c7label.setFont(QFont(shell_font, pointSize=16))
        self.c7label.setAlignment(QtCore.Qt.AlignCenter)
##        self.c7.setStyleSheet("QPushButton"
##                             "{"
##                             "background-color : lightblue;"
##                             "}"
##                             "QPushButton::pressed"
##                             "{"
##                             "background-color : red;"
##                             "}"
##                             )
        

        #layout 1 row at a time

        layout.addWidget(title,                    0, 2, 1, 2)

        layout.addWidget(freqText,                 1, 0, 1, 2)
        layout.addWidget(self.freqInput,           2, 0, 1, 2)
        layout.addWidget(self.c2,                  2, 2, 1, 1)

        layout.addWidget(powerText,                1, 3, 1, 2)
        layout.addWidget(self.powerInput,          2, 3, 1, 2)
        layout.addWidget(self.c3,                  2, 5, 1, 1)

        layout.addWidget(onoffText,                3, 0, 1, 2)
        layout.addWidget(self.onoffNotif,               4, 0, 1, 2)
        layout.addWidget(self.c4,                  5, 0, 1, 1)
        layout.addWidget(self.c5,                  5, 1, 1, 1)

        layout.addWidget(chanText,                 3, 3, 1, 2)
        layout.addWidget(self.chanNotif,                4, 3, 1, 2)
        layout.addWidget(self.c6,                  5, 3, 1, 1)
        layout.addWidget(self.c7,                  5, 4, 1, 1)
        

##        layout.addWidget(self.c2label,                  4, 1, 1, 1)
##        layout.addWidget(self.c3label,                  4, 4, 1, 1)
##        layout.addWidget(self.c4label,                  3, 6, 1, 1)
##        layout.addWidget(self.c5label,                  4, 7, 1, 1)



        layout.minimumSize()

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = QCustomWindfreakGui()
    icon.show()
    app.exec_()

