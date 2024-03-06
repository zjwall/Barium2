
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
       self.setMaximumHeight(30)

       
class StretchedLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setMinimumSize(QSize(350, 100))

    def resizeEvent(self, evt):

        font = self.font()
        font.setPixelSize(self.width() * 0.14 - 14)
        self.setFont(font)

        
class RFGui(QFrame):
    """
    GUI for a single DDS channel (Urukul).
    """

    def __init__(self, name=None, parent=None):
        QWidget.__init__(self, parent)
        self.name = name
        self.setFrameStyle(0x0001 | 0x0030)
        self.setMaximumSize(500, 175)
        self.makeLayout()

    def makeLayout(self):
        layout = QGridLayout(self)
        title = QLabel('Trap RF')
        title.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        title.setAlignment(Qt.AlignCenter)
        chan_label = QLabel(self.name)
        chan_label.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        chan_label.setAlignment(QtCore.Qt.AlignCenter)
        freqlabel = QLabel('Frequency (MHz)')
        powerlabel = QLabel('Power (dBm)')
        
        # editable fields
        self.amp = QDoubleSpinBox()
        self.amp.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        self.amp.setDecimals(5)
        self.amp.setSingleStep(.1)
        self.amp.setRange(-100.0, 8.0)
        self.amp.setKeyboardTracking(False)
        self.amp.setAlignment(Qt.AlignRight)


        
        layout.addWidget(freqlabel,1, 0, 1, 1)
        layout.addWidget(powerlabel,1, 1, 1, 1)
        
        self.freq = QDoubleSpinBox()
        self.freq.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        self.freq.setDecimals(5)
        self.freq.setSingleStep(.01)
        self.freq.setRange(1, 3000)
        self.freq.setKeyboardTracking(False)
        self.freq.setAlignment(Qt.AlignRight)
        
        # buttons
        self.on_switch = TextChangingButton(('On','Off'))
        self.on_switch.setFont(QFont('MS Shell Dlg 2', pointSize=10))

        layout.addWidget(title,0,0)

        # add widgets to layout
        layout.addWidget(chan_label, 2, 0)
        layout.addWidget(self.freq, 2, 0)
        layout.addWidget(self.amp, 2, 1)
        layout.addWidget(self.on_switch, 2, 2)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = RFGui()
    icon.show()
    app.exec_()
