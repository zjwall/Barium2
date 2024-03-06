import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout


#####Big Note -----when using tabswidget in pyqt5 your widget can't have show() or they will wierdly overlap the tabs
# Creating the main window
class artiq_client(QMainWindow):
    def __init__(self, reactor, parent=None):
            super(artiq_client,self).__init__()
            self.title = 'ARTIQ'
            self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
            self.setWindowTitle(self.title)

            self.tab_widget = MyTabWidget(self)
            self.setCentralWidget(self.tab_widget)

            self.show()


        
# Creating tab widgets
class MyTabWidget(QWidget):
    def __init__(self, parent):
            super(QWidget, self).__init__(parent)
            self.layout = QGridLayout(self)

            # Initialize tab screen
            self.tabs = QTabWidget()
            self.tab1 = self.makeTrapControlWidget(reactor)
            self.tab2 = self.makeTTLWidget(reactor)
            self.tab3 = self.makeDDSWidget(reactor)
            #self.tabs.resize(300, 200)

            # Add tabs
            self.tabs.addTab(self.tab1, "DAC")
            self.tabs.addTab(self.tab2, "TTL")
            self.tabs.addTab(self.tab3, "DDS")


            # Add tabs to widget
            self.layout.addWidget(self.tabs)
            self.setLayout(self.layout)


    def makeTrapControlWidget(self, reactor):
        from trap_client import Trap_client
        trap = Trap_client(reactor)
        return trap

    def makeTTLWidget(self, reactor):
        from artiq_ttl_client import TTL_client
        ttl = TTL_client(reactor)
        return ttl

    def makeDDSWidget(self, reactor):
        from artiq_dds_client import DDS_client
        dds = DDS_client(reactor)
        return dds
    
if __name__ == '__main__':
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor  
    client_inst = artiq_client(reactor)
    client_inst.show()
    reactor.run()
