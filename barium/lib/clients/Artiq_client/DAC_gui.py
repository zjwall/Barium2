
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

        
class DAC_channel(QFrame):
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
        
        dac_label = QLabel(self.name)
        dac_label.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        dac_label.setAlignment(QtCore.Qt.AlignCenter)

        # editable fields
        self.dac = QDoubleSpinBox()
        self.dac.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        self.dac.setDecimals(5)
        self.dac.setSingleStep(.1)
        self.dac.setRange(-10, 10)
        self.dac.setKeyboardTracking(False)
        self.dac.setAlignment(Qt.AlignRight)



        # buttons
        self.on_switch = TextChangingButton(('On','Off'))
        self.on_switch.setFont(QFont('MS Shell Dlg 2', pointSize=10))


        # add widgets to layout
        layout.addWidget(dac_label, 0, 0)
        layout.addWidget(self.dac, 0, 1)
        layout.addWidget(self.on_switch, 0, 2)





class DACGui(QFrame):
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


        title = QLabel('ARTIQ DAC')
        title.setFont(QFont('MS Shell Dlg 2', pointSize=16))
        title.setAlignment(Qt.AlignCenter)
        self.channels = []
        for i in range(32):
            self.channels.append(DAC_channel('ch ' + str(i)))
            if i > 7:  
                layout.addWidget(self.channels[i], i+1-8, 1)
            if i > 15:
                layout.addWidget(self.channels[i], i+1-16, 2)
            if i > 23:
                layout.addWidget(self.channels[i], i+1-24, 3)
            if i < 8:
                layout.addWidget(self.channels[i], i+1, 0)


        layout.addWidget(title,0,0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    icon = DACGui()
    icon.show()
    app.exec_()
