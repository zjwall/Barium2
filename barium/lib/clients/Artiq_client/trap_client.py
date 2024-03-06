import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout



        
# Creating tab widgets
class Trap_client(QWidget):
    def __init__(self, reactor, parent=None):
            super(QWidget, self).__init__()
            self.layout = QGridLayout(self)
            self.layout.addWidget(self.makeDACWidget(reactor),0,1)
            self.layout.addWidget(self.makeRFWidget(reactor),0,0)

            



            # Add tabs to widget
            self.setLayout(self.layout)
            self.show()


    def makeDACWidget(self, reactor):
        from artiq_dac_client import DAC_client
        dac = DAC_client(reactor)
        return dac

    def makeRFWidget(self, reactor):
        from RF_client import RF_client 
        rf = RF_client(reactor)
        return rf


    
if __name__ == '__main__':
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = Trap_client(reactor)
    client_inst.show()
    reactor.run()
