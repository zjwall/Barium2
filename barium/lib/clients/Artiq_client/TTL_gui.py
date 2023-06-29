
import sys
from PyQt5 import QtGui, QtCore

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
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

        
class TTL_channel(QFrame):
    """
    GUI for a single AD5372 DAC channel (Zotino).
    """

    def __init__(self, name=None, parent=None):
        QWidget.__init__(self, parent)
        self.name = name
        self.setFrameStyle(0x0001 | 0x0030)
        self.setMaximumSize(400, 175)
        self.makeLayout()

    def makeLayout(self):
        layout = QGridLayout(self)
        



        # buttons
        self.on_switch = TextChangingButton((self.name,self.name))
        self.on_switch.setFont(QFont('MS Shell Dlg 2', pointSize=10))


        # add widgets to layout
        layout.addWidget(self.on_switch, 0, 2)





class TTLGui(QFrame):
    """
    GUI for all DAC channels (i.e. a Fastino or Zotino).
    """

    name = "Zotino GUI"

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setFrameStyle(0x0001 | 0x0030)
        self.makeLayout()

    def makeLayout(self):
        layout = QGridLayout(self)


        title = QLabel('ARTIQ TTLS')
        title.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        title.setAlignment(Qt.AlignCenter)
        self.channels = []
        for i in range(20):
            self.channels.append(TTL_channel('ch ' + str(i+4)))
            if i > 4:  
                layout.addWidget(self.channels[i], i+1-5, 1)
            if i > 9:
                layout.addWidget(self.channels[i], i+1-10, 2)
            if i > 14:
                layout.addWidget(self.channels[i], i+1-15, 3)
            if i < 5:
                layout.addWidget(self.channels[i], i+1, 0)


        layout.addWidget(title,0,0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = TTLGui()
    icon.show()
    app.exec_()
