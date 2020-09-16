# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.qlabel = QLabel('None Selected', self)
        self.title = 'PyQt5 image - pythonspot.com'
        self.left = 10
        self.top = 40
        self.width = 640
        self.height = 480
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create widget
        label = QLabel(self)
        pixmap = QPixmap(r"C:\Users\Max Marno\Documents\Projects\GSV\TESTIMAGE.png")

        label.setPixmap(pixmap)
        self.resize(pixmap.width(),pixmap.height())
        
        self.show()
        self.mousePressEvent = self.getPos
    # from https://stackoverflow.com/questions/3504522/pyqt-get-pixel-position-and-value-when-mouse-click-on-the-image
    def getPos(self, event):
        x = event.pos().x()
        y = event.pos().y()
        global imgcoords
        imgcoords = [x,y]
        self.xxyy = imgcoords
        self.title = str(imgcoords)
        self.qlabel.setText(str(imgcoords))
        self.setWindowTitle(str(imgcoords))
        #Not necessary to 'update' the setWindowTitle does it automatically
        
        #self.update()
        #print(x)
        #print(y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    
    sys.exit(app.exec_())