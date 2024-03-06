"""
Reworked code based on
http://trevorius.com/scrapbook/uncategorized/pyqt-custom-abstractitemmodel/
Adapted to Qt5 and fixed column/row bug.
TODO: handle changing data.
"""
from scripting_widget import scripting_widget
from common.lib.clients.connection import connection
from tree_view.Controllers import ParametersEditor
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import *

class Node(object):
    def __init__(self, name, parent=None): 
        super(Node, self).__init__()
        from labrad.units import WithUnit
        self.WithUnit = WithUnit
        self._name = name
        self._children = []
        self._parent = parent
        if parent is not None:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)
        child._parent = self

    def insertChild(self, position, child):
        print('got here')
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        child._parent = None
        return True

    def name(self):
        return self._name
    
    def filter_text(self):
        return self.name()

    def child(self, row):
        try:
            return self._children[row]
        except IndexError:
            return None
    
    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent
    
    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def data(self, column):
        if column == 0: return self.name()
    
    def setData(self, column, value):
        pass
    
    def clear_data(self):
        del self._children[:]

class CollectionNode(Node):
    def __init__(self, name, parent = None):
        super(CollectionNode, self).__init__(name, parent)
    
    def filter_text(self):
        return ''.join([child.filter_text() for child in self._children])

class CustomNode(object):
    def __init__(self, data):
        self._data = data
        if type(data) == tuple:
            self._data = list(data)
        if type(data) is str or not hasattr(data, '__getitem__'):
            self._data = [data]

        self._columncount = len(self._data)
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if column >= 0 and column < len(self._data):
            return self._data[column]

    def columnCount(self):
        return self._columncount

    def childCount(self):
        return len(self._children)

    def child(self, row):
        if row >= 0 and row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)
        self._columncount = max(child.columnCount(), self._columncount)


class CustomModel(QtCore.QAbstractItemModel):
    def __init__(self, nodes):
        QtCore.QAbstractItemModel.__init__(self)
        self._root = CustomNode(None)
        for node in nodes:
            self._root.addChild(node)

    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().childCount()
        return self._root.childCount()

    def addChild(self, node, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        parent.addChild(node)

    def index(self, row, column, _parent=None):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QtCore.QModelIndex()

        child = parent.child(row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, index):
        if index.isValid():
            return index.internalPointer().columnCount()
        return self._root.columnCount()

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == QtCore.Qt.DisplayRole:
            return node.data(index.column())
        return None
    def addData(self, name, parent_index=QModelIndex()):
        position = 3
        new = CustomNode("hi")
        new.addChild(CustomNode(['1', '2', '3']))
        self.beginInsertRows(parent_index, position, position)
        self.addChild(new, None)
        self.endInsertRows()
        #self.layoutChanged.emit()


class ParametersTreeModel(QAbstractItemModel):
    
    filterRole  = Qt.UserRole
    on_new_parameter = pyqtSignal(tuple, tuple)
    
    def __init__(self, root, parent=None):
        QtCore.QAbstractItemModel.__init__(self)
        #super(ParametersTreeModel, self).__init__(parent)
        self._rootNode = root
        
    def rowCount(self, parent):
        '''
        returns the count
        '''
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()
        return parentNode.childCount()

    def columnCount(self, parent):
        return 2
        
    def data(self, index, role):
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == Qt.DisplayRole or role == Qt.EditRole:
            return node.data(index.column())
        
        if role == ParametersTreeModel.filterRole:
            return node.filter_text()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            node = index.internalPointer()
            if role == Qt.EditRole:
                node.setData(index.column(), value)
                textIndex = self.createIndex(index.row(), 1, index.internalPointer())
                self.dataChanged.emit(index, index)
                self.dataChanged.emit(textIndex, textIndex)
                if not isinstance(node, CollectionNode):
                    self.on_new_parameter.emit(node.path(), node.full_parameter())
                return True
        return False

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if section == 0:
                return "Collection"
            else:
                return "Value"

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def parent(self, index):      
        '''
        returns the index of the parent of the node at the given index
        '''
        node = self.getNode(index)
        parentNode = node.parent()
        if parentNode == self._rootNode:
            return QModelIndex()
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    def index(self, row, column, parent): 
        '''
        returns the index for the given parent, row and column
        '''
        parentNode = self.getNode(parent)
        childItem = parentNode.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def getNode(self, index):
        '''
        returns node of the given index
        '''
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node            
        return self._rootNode

    def insert_collection(self, name, parent_index=QModelIndex()):
        parentNode = self.getNode(parent_index)
        row_count = self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = CustomNode(name)
        print('breaks here')
        self.endInsertRows()
        print('endinsert')
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_parameter(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        print('insert param')
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = ParameterNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index

    def insert_event(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = EventNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index

    def insert_scan(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = ScanNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_bool(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = BoolNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_string(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = StringNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_selection_simple(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = SelectionSimpleNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_line_selection(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = LineSelectionNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index

    def insert_sideband_selection(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = SidebandElectorNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_duration_bandwidth(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = DurationBandwidthNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def insert_spectrum_sensitivity(self, parameter_name, info, parent_index):
        collectionNode = self.getNode(parent_index)
        row_count =  self.rowCount(parent_index)
        self.beginInsertRows(parent_index, row_count, row_count)
        childNode = SpectrumSensitivityNode(parameter_name, info, collectionNode)
        self.endInsertRows()
        index = self.index(row_count, 0, parent_index)
        return index
    
    def set_parameter(self, index, info):
        node = index.internalPointer()
        node.set_full_info(info)
        #refresh all columns
        max_index= self.createIndex(index.row(), node.columns, index.internalPointer())
        self.dataChanged.emit(index, max_index)
        
    def clear_model(self):
        rows = self._rootNode.childCount()
        self.beginRemoveRows(QModelIndex(), 0, rows)
        self._rootNode.clear_data()
        self.endRemoveRows()
    def addData(self, name, parent_index=QModelIndex()):
        position = 3
        new = CollectionNode("hi")
        self.beginInsertRows(parent_index, position, position)
        self._rootNode.addChild(new)
        self.endInsertRows()
        #self.layoutChanged.emit()

class MyTree():
    """
    """
    def __init__(self):
        self.items = []

        # Set some random data:
        for i in 'abc':
            self.items.append(CustomNode(i))
            self.items[-1].addChild(CustomNode(['d', 'e', 'f']))
            self.items[-1].addChild(CustomNode(['g', 'h', 'i']))
            
        root = CollectionNode("Root")
        self.tw = ParametersEditor()
        self.tw.setModel(ParametersTreeModel(root))
        #self.tw.model().insert_collection('tik')
        self.tw.model().addData('hi')

    def add_data(self, data):
        """
        TODO: how to insert data, and update tree.
        """
        #self.items[-1].addChild(CustomNode(['1', '2', '3']))
        #self.tw.setModel(CustomModel(self.items))
        model = self.tw.model()
        rootIdx = model.index(0, 0, QtCore.QModelIndex())
        position = 3
        new = CustomNode("new")
        new.addChild(CustomNode(['1', '2', '3']))
        model.beginInsertRows(rootIdx, position, position)
        model.addChild(new, None)
        model.endInsertRows()
        model.layoutChanged.emit()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mytree = MyTree()
    mytree.tw.show()
    sys.exit(app.exec_())
