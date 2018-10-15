#!/usr/bin/env python
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QGridLayout
from PyQt5.QtGui import QIcon
from PyQt5 import QtCore

class Gui(QMainWindow):
    '''Create a window and display the title of the project in the center'''

    def __init__(self):
        super().__init__()
        self.title = ''
        self.left = 10
        self.top = 10
        self.width = 440
        self.height = 280
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #create a QWidget and set it as a central widget
        #we need the QWidget becasue you cannot set a QLayout directly on QMainWindow
        centralWidget = QWidget(self) 
        self.setCentralWidget(centralWidget)

        #set up a GridLayout 
        gridLayout = QGridLayout()

        label = QLabel('SIG Blockchain Project', self)
        gridLayout.addWidget(label, 0, 0, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

        centralWidget.setLayout(gridLayout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())
