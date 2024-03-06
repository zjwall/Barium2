from twisted.internet.defer import inlineCallbacks
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication

class signalWidget(QWidget):
    
    SERVER_CONNECT_ID = 9898989
    SERVER_DISCONNECT_ID = 9898990
    
    def __init__(self, reactor, parent=None):
        super(signalWidget, self).__init__(parent)
        self.reactor = reactor
        self.setupLayout()
        self.connect()
    
    def setupLayout(self):
        #setup the layout and make all the widgets
        self.setWindowTitle('Test')
        #create a horizontal layout
        layout = QHBoxLayout()
        #create the text widget 
        self.textedit = QTextEdit()
        self.textedit.setReadOnly(True)
        layout.addWidget(self.textedit)
        self.setLayout(layout)
        
    @inlineCallbacks
    def connect(self):
        #make an asynchronous connection to LabRAD
        from labrad.wrappers import connectAsync
        #cxn = yield connectAsync(host='localhost',name = 'Signal Widget')
        #cxn = yield connectAsync('flexo', name = 'Test', password='lab')
        self.wm_cxn = yield connectAsync(multiplexer_config.ip, name =  ' Single Channel Lock', password='lab')
        self.wm = yield self.wm_cxn.multiplexerserver
        manager = cxn.manager
        #subscribe to 'Server Connect' message
        yield manager.subscribe_to_named_message('Server Connect', self.SERVER_CONNECT_ID, True)
        yield manager.addListener(listener = self.followServerConnect, source = None, ID = self.SERVER_CONNECT_ID)
        #subscribe to 'Server Disconnect' message
        yield manager.subscribe_to_named_message('Server Disconnect', self.SERVER_DISCONNECT_ID, True)
        yield manager.addListener(listener = self.followServerDisconnect, source = None, ID = self.SERVER_DISCONNECT_ID)
    
    def followServerConnect(self, cntx, server_name):
        #executed when a server connects to the manager
        server_name = server_name[1]
        text =  'Server Connected: {}'.format(server_name)
        self.textedit.append(text)
    
    def followServerDisconnect(self, cntx, server_name):
        #executed when the server disconnected from the manager
        server_name = server_name[1]
        text = 'Server Disconnected: {}'.format(server_name)
        self.textedit.append(text)
        
    def closeEvent(self, x):
        #stop the reactor when closing the widget
        self.reactor.stop()

if __name__=="__main__":
    #join Qt and twisted event loops
    a = QApplication( [] )
    import qt5reactor
    qt5reactor.install()
    from twisted.internet import reactor
    widget = signalWidget(reactor)
    widget.show()
    reactor.run()
