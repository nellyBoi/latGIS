# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt



class ImageScroller(QtWidgets.QWidget):
    def __init__(self):
        self.chosen_points = []
        QtWidgets.QWidget.__init__(self)
        self._image = QtGui.QPixmap(r"C:\Users\Max Marno\Documents\Projects\GSV\TESTIMAGE.png")

    def paintEvent(self, paint_event):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(self.rect(), self._image)
        pen = QtGui.QPen()
        pen.setColor(QColor(255, 0, 0, 127))
        pen.setWidth(20)
        
        painter.setPen(pen)
        #painter.setBrush(Qt.CrossPattern)
        #painter.setBrush(Qt.red)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        
        #painter.drawPoint(300, 300)
        #painter.drawLine(100, 100, 400, 400)
        for pos in self.chosen_points:
            painter.drawPoint(pos)
            #painter.drawEllipse(pos, 10,10)

    def mouseReleaseEvent(self, cursor_event):
        self.chosen_points.append(cursor_event.pos())
        # self.chosen_points.append(self.mapFromGlobal(QtGui.QCursor.pos()))
        self.update()
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_D:
            print('Delete Last Point')
            self.chosen_points.pop()
        self.update()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = ImageScroller()
    w.resize(640, 480)
    w.show()
    #sys.exit(app.exec_())