#!/usr/bin/env python
#-*- coding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, QGridLayout
from twisted.internet.defer import inlineCallbacks, returnValue
import socket
import os
import twisted

from scripting_widget import scripting_widget
from common.lib.clients.connection import connection
from tree_view.Controllers import ParametersEditor
from tree_view.Data import ParameterNode, CollectionNode, ScanNode, BoolNode


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
            parentNode = self.ParametersEditor._model.getNode(QModelIndex())
            #self.ParametersEditor._model.beginInsertRows(QModelIndex(), 0 ,0)
            #childNode = CollectionNode('tik', parentNode)
            #self.ParametersEditor._model.endInsertRows()
            print('error here3')
        except Exception as e:
            print(e)
            raise
            print('script_scanner_gui: servers not available')
            
    @inlineCallbacks
    def populateParameters(self):
        pv = yield self.cxn.get_server('ParameterVault')
        collections = yield pv.get_collections(context=self.context)
        print(collections)
        for collection in collections:
            print('add collection')
            self.ParametersEditor.add_collection_node(collection)
            print('addcollection')
            parameters = yield pv.get_parameter_names(collection)
            for param_name in parameters:
                print('get param')
                value = yield pv.get_parameter(collection, param_name, False)
                self.ParametersEditor.add_parameter(collection,
                                                    param_name, value)
                print('again')
            print('su')


if __name__ == "__main__":
    a = QApplication( sys.argv )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    gui = test_gui(reactor)
    gui.show()
    reactor.run()
