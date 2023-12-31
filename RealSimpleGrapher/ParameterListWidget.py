import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

from twisted.internet.defer import inlineCallbacks, returnValue, DeferredLock, Deferred
from queue import Queue

class ParameterList(QWidget):
    
    def __init__(self, dataset):
        super(ParameterList, self).__init__()
        self.dataset = dataset
        mainLayout = QtGui.QVBoxLayout() 
        self.parameterListWidget = QtGui.QListWidget()
        mainLayout.addWidget(self.parameterListWidget)        
        self.setWindowTitle(str(dataset.dataset_name))# + " " + str(dataset.directory))
        self.populate()
        self.setLayout(mainLayout)
        self.show()

    @inlineCallbacks
    def populate(self):
        parameters = yield self.dataset.getParameters()
        self.parameterListWidget.clear()
        self.parameterListWidget.addItems([str(x) for x in sorted(parameters)])
