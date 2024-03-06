import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QLabel
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

from Data import ParameterNode, CollectionNode, ScanNode, BoolNode
from Data import StringNode, SelectionSimpleNode, LineSelectionNode, SidebandElectorNode, EventNode
from Data import DurationBandwidthNode, SpectrumSensitivityNode
from tree_view.Controllers import ParametersEditor

class test_gui(QWidget):

    def __init__(self, reactor, cxn=None):
        super(test_gui, self).__init__()
        self.cxn = cxn
        self.reactor = reactor
        self.setupWidgets()
        self.connect()

    def setupWidgets(self):
        self.ParametersEditor = ParametersEditor(self.reactor)
        layout = QHBoxLayout()
        layout.addWidget(self.ParametersEditor)
        self.setLayout(layout)
        self.setWindowTitle('Script Scanner Gui')

    @inlineCallbacks
    def connect(self):
        from labrad.units import WithUnit
        from labrad.types import Error
        self.WithUnit = WithUnit
        self.Error = Error
        self.subscribedScriptScanner = False
        self.subscribedParametersVault = False
        if self.cxn is None:
            self.cxn = connection()
            yield self.cxn.connect()
        self.context = yield self.cxn.context()
        try:
            print('error here2')
            #yield self.populateParameters()
            print('error here3')
        except Exception as e:
            print(e)
            raise
            print('script_scanner_gui: servers not available')


if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    gui = test_gui(reactor)
    gui.show()
    reactor.run()
