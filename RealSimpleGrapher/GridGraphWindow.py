'''
Window containing a grid of graphs
'''
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout

from GraphWidgetPyQtGraph import Graph_PyQtGraph as Graph
from ScrollingGraphWidgetPyQtGraph import ScrollingGraph_PyQtGraph as ScrollingGraph
import GUIConfig
from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.internet.task import LoopingCall
from twisted.internet.threads import blockingCallFromThread
from queue import Queue

class GridGraphWindow(QWidget):
    def __init__(self, g_list, row_list, column_list, reactor, parent=None):
        super(GridGraphWindow, self).__init__(parent)
        self.reactor = reactor        
        self.initUI(g_list, row_list, column_list)
        self.show()

    def initUI(self, g_list, row_list, column_list):
        reactor = self.reactor
        layout = QGridLayout()
        for k in range(len(g_list)):
            layout.addWidget(g_list[k], row_list[k], column_list[k])
        self.setLayout(layout)

