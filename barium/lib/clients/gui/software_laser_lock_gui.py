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


class software_laser_lock_channel(QFrame):
    def __init__(self, chanName,  parent = None):
        window = QWidget.__init__(self, parent)
        self.setFrameStyle(0x0001 | 0x0030)
        self.makeLayout(chanName)

    def makeLayout(self, name):
        layout = QGridLayout()

        shell_font = 'MS Shell Dlg 2'
        chanName = QLabel(name)
        chanName.setFont(QFont(shell_font, pointSize=12))
        chanName.setAlignment(QtCore.Qt.AlignCenter)

        self.wavelength = QLabel('frequency')
        self.wavelength.setFont(QFont(shell_font,pointSize=64))
        self.wavelength.setAlignment(QtCore.Qt.AlignCenter)
        self.wavelength.setStyleSheet('color: blue')

        # Create lock button
        self.lockSwitch = TextChangingButton(('Locked','Unlocked'))


        #frequency switch label
        lockName = QLabel('Lock Frequency')
        lockName.setFont(QFont(shell_font, pointSize=12))
        lockName.setAlignment(QtCore.Qt.AlignCenter)

        # frequency
        self.spinFreq1 =QDoubleSpinBox()
        self.spinFreq1.setFont(QFont(shell_font, pointSize=12))
        self.spinFreq1.setDecimals(6)
        self.spinFreq1.setSingleStep(1e-6)
        self.spinFreq1.setRange(0, 1e4)
        self.spinFreq1.setKeyboardTracking(False)

        #exposure label
        exposureName = QLabel('Exposure')
        exposureName.setFont(QtGui.QFont(shell_font, pointSize=12))
        exposureName.setAlignment(QtCore.Qt.AlignCenter)

        # exposure
        self.spinExposure = QDoubleSpinBox()
        self.spinExposure.setFont(QFont(shell_font, pointSize=12))
        self.spinExposure.setDecimals(0)
        self.spinExposure.setSingleStep(1)
        self.spinExposure.setRange(0, 2000)
        self.spinExposure.setKeyboardTracking(False)

        #gain  label
        gainName = QLabel('Gain')
        gainName.setFont(QFont(shell_font, pointSize=12))
        gainName.setAlignment(QtCore.Qt.AlignCenter)

        # gain
        self.spinGain = QDoubleSpinBox()
        self.spinGain.setFont(QFont(shell_font, pointSize=12))
        self.spinGain.setDecimals(6)
        self.spinGain.setSingleStep(1e-6)
        self.spinGain.setRange(1e-6, 1)
        self.spinGain.setKeyboardTracking(False)

        #rails  label
        lowRail = QLabel('Low Rail')
        lowRail.setFont(QFont(shell_font, pointSize=12))
        lowRail.setAlignment(QtCore.Qt.AlignCenter)


        # low rail
        self.spinLowRail = QDoubleSpinBox()
        self.spinLowRail.setFont(QFont(shell_font, pointSize=12))
        self.spinLowRail.setDecimals(3)
        self.spinLowRail.setSingleStep(.001)
        self.spinLowRail.setRange(0 , 100)
        self.spinLowRail.setKeyboardTracking(False)

        #high rails  label
        highRail = QLabel('High Rail')
        highRail.setFont(QFont(shell_font, pointSize=12))
        highRail.setAlignment(QtCore.Qt.AlignCenter)


        # high rail
        self.spinHighRail = QDoubleSpinBox()
        self.spinHighRail.setFont(QFont(shell_font, pointSize=12))
        self.spinHighRail.setDecimals(3)
        self.spinHighRail.setSingleStep(.001)
        self.spinHighRail.setRange(0 , 100)
        self.spinHighRail.setKeyboardTracking(False)


        #dac voltage  label
        setDacVoltage = QLabel(' Set Dac Voltage')
        setDacVoltage.setFont(QtGui.QFont(shell_font, pointSize=12))
        setDacVoltage.setAlignment(QtCore.Qt.AlignCenter)

        # set dac voltage
        self.spinDacVoltage = QDoubleSpinBox()
        self.spinDacVoltage.setFont(QFont(shell_font, pointSize=12))
        self.spinDacVoltage.setDecimals(3)
        self.spinDacVoltage.setSingleStep(.001)
        self.spinDacVoltage.setRange(0 , 100)
        self.spinDacVoltage.setKeyboardTracking(False)

        # Too lazy to add signals to the server so
        # will update and display dac voltage every time
        # frequency updates
        self.dacLabel = QLabel('Dac Voltage')
        self.dacLabel.setFont(QFont('MS Shell Dlg 2',pointSize=14))
        self.dacLabel.setAlignment(QtCore.Qt.AlignCenter)


        self.dacVoltage = QLabel('0.0')
        self.dacVoltage.setFont(QFont('MS Shell Dlg 2',pointSize=14))
        self.dacVoltage.setAlignment(QtCore.Qt.AlignCenter)


        # clear lock button for voltage stuck too high
        self.clear_lock = QPushButton('Clear Lock Voltage')
        self.clear_lock.setMaximumHeight(30)
        self.clear_lock.setFont(QFont('MS Shell Dlg 2', pointSize=12))


        
        layout.addWidget(chanName, 1,1)
        layout.addWidget(self.wavelength, 2,0, 6, 2)
        layout.addWidget(self.lockSwitch, 1, 3, 1, 1)
        layout.addWidget(lockName, 10, 0, 1, 1)
        layout.addWidget(self.spinFreq1, 11, 0, 1, 1)
        layout.addWidget(exposureName, 10, 1, 1, 1)
        layout.addWidget(self.spinExposure, 11, 1, 1, 1)
        layout.addWidget(gainName, 2, 3, 1, 1)
        layout.addWidget(self.spinGain, 3, 3, 1, 1)
        layout.addWidget(lowRail, 4, 3, 1, 1)
        layout.addWidget(self.spinLowRail, 5, 3, 1, 1)
        layout.addWidget(highRail, 6, 3, 1, 1)
        layout.addWidget(self.spinHighRail, 7, 3, 1, 1)
        layout.addWidget(setDacVoltage, 8, 3, 1, 1)
        layout.addWidget(self.spinDacVoltage, 9, 3, 1, 1)
        layout.addWidget(self.dacLabel, 10,3, 1, 1)
        layout.addWidget(self.dacVoltage, 11,3, 1, 1)
        layout.addWidget(self.clear_lock, 1, 0, 1, 1)

        layout.minimumSize()

        self.setLayout(layout)
if __name__ == "__main__":

    app= QApplication(sys.argv)
    
    icon = software_laser_lock_channel('cooling laser')
    icon.show()
    app.exec_()
    
   
    
    
