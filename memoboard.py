from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import glob
import sys

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.time = QDate.currentDate()
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setWindowTitle('Memoboard')
        message = "{0}     {1}".format("Ready", self.time.toString(Qt.DefaultLocaleLongDate))
        self.statusBar().showMessage(message)
        self.resize(1000,927)
        self.center()

        self.status()

        self.show()

    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())

    def status(self):
        self.centralWidget = QWidget(self)
        labels = [QLabel(self.centralWidget) for i in range(6)]
        for idx,item in enumerate(labels):
            item.setStyleSheet("color: black;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: #FA8072;"
                              "border-radius: 3px")
            item.setText("뀨:{}".format(idx))

        hbox = QHBoxLayout(self.centralWidget)
        hboxaddwidget = [hbox.addWidget(i) for i in labels]

        self.setCentralWidget(self.centralWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())