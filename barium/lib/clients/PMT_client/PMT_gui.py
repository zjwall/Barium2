
import sys
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from common.lib.clients.qtui.q_custom_text_changing_button import TextChangingButton 

class TextChangingButton(TextChangingButton):
    def __init__(self, button_text=None, parent=None):
       super(TextChangingButton, self).__init__(button_text, parent)
       self.setMaximumHeight(50)

       
class StretchedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setMinimumSize(QSize(350, 100))

    def resizeEvent(self, evt):

        font = self.font()
        font.setPixelSize(self.width() * 0.14 - 14)
        self.setFont(font)

        
class PMTGui(QFrame):
    """
    GUI for a single AD5372 DAC channel (Zotino).
    """

    def __init__(self, name=None, parent=None):
        QWidget.__init__(self, parent)
        self.name = name
        self.setFrameStyle(0x0001 | 0x0030)
        self.setMaximumSize(400, 400)
        self.makeLayout()
        self.setGeometry(600,1500,500,400)

    def makeLayout(self):
        layout = QGridLayout(self)
        

        self.title = QLabel('PMT')
        self.title.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        self.title.setAlignment(Qt.AlignCenter)        # display
        self.title.resize(100,400)
        self.count_display = QLCDNumber()
        self.count_display.setDigitCount(10)
        self.count_display.display('OFF')

        # buttons
        self.on_switch = TextChangingButton(('On','Off'))
        self.on_switch.setFont(QFont('MS Shell Dlg 2', pointSize=10))

        self.record = TextChangingButton('Record')
        self.record.setFont(QFont('MS Shell Dlg 2', pointSize=10))

        
        # add widgets to layout
        layout.addWidget(self.title,0,0)
        layout.addWidget(self.count_display, 1, 0)
        layout.addWidget(self.on_switch, 2, 0)
        layout.addWidget(self.record, 3, 0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = PMTGui()
    icon.show()
    app.exec_()
