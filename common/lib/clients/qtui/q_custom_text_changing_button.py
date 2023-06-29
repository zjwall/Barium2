
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class TextChangingButton(QtWidgets.QPushButton):
     
    #"""Button that changes its text to ON or OFF and colors when it's pressed.
    # """
    def __init__(self, button_text, parent=None):
       # """
       # NOTE: when both labels and addtext are not None, labels take
       # precedence.

       # Parameters
       #----------
       # button_text: could be a 2-tuple of string, a string, or None.
           # When it's a 2-tuple, the first entry corresponds to text when the
           # button is "ON", and the second entry corresponds to text when the
           # button is "OFF".
            #When it's a string, it is the text that gets added before "ON" or
           # "OFF".
       # """
      btn = QtWidgets.QPushButton('Button')
      super(TextChangingButton, self).__init__()
      self.button_text = button_text
      self.setCheckable(True)
      self.setFont(QFont('MS Shell Dlg 2', pointSize=10))
      self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
      #connect signal for appearance changing
      self.toggled.connect(self.setAppearance)
      self.setAppearance(self.isDown())

    def setAppearance(self, down):
        on_text, off_text = self._set_button_texts()
        if down:
            self.setText(on_text)
            self.setPalette(QPalette(Qt.darkGreen))
            self.setStyleSheet("color: black;")
        else:
            self.setText(off_text)
            self.setPalette(QPalette(Qt.black))
            self.setStyleSheet("color: black;")

    def _set_button_texts(self):
        #"""Return button texts when they are on or off."""
        if type(self.button_text) == str:
            on_text = self.button_text + "   On"
            off_text = self.button_text + "   Off"
        elif type(self.button_text) == tuple:
            on_text = self.button_text[0]
            off_text = self.button_text[1]
        elif self.button_text is None:
            on_text = "On"
            off_text = "Off"
        else:
            error_msg = "Text gets displayed on a button needs to be a string"
            raise TypeError(error_msg)
        return on_text, off_text

   # def sizeHint(self):
       # return QSize(37, 26)


##if __name__ == "__main__":
##    app = QApplication(sys.argv)
##    myapp = TextChangingButton()
##    myapp.show()
##    sys.exit(app.exec_())
##
