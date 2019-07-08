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
        self.resize(774,879)
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

        status = ["대사관","아포스티유","공증","등기","견적서","계산서"]
        status_stylesheet = {"대사관":"color: black;"              #빨간색
                                "background-color: #7EB9FF;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #7EB9FF;"
                                "border-radius: 8px",
                        "아포스티유":"color: black;"           #주황색
                                "background-color: #ff917b;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #ff917b;"
                                "border-radius: 8px",
                        "공증": "color: black;"               #초록색
                                "background-color: #b3eb2b;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #b3eb2b;"
                                "border-radius: 8px",
                        "등기": "color: black;"               #보라색
                                "background-color: #C486FF;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #C486FF;"
                                "border-radius: 8px",
                        "견적서": "color: black;"             #노란색
                                "background-color: #FEFF7F;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #FEFF7F;"
                                "border-radius: 8px",
                        "계산서": "color: black;"             #노란색
                                "background-color: #FEFF7F;"
                                "border-style: solid;"
                                "border-width: 3px;"
                                "border-color: #FEFF7F;"
                                "border-radius: 8px"
                        }

        labels = [QLabel(self.centralWidget) for i in range(6)]
        for idx,item in enumerate(labels):
            font = QFont()
            font.setFamily("맑은 고딕")
            font.setPointSize(18)
            font.setBold(True)

            item.setFont(font)
            item.setStyleSheet(status_stylesheet[status[idx]])
            item.setText("{}".format(status[idx]))
            item.setAlignment(Qt.AlignCenter)
            print(item.x())

        print(status_stylesheet["계산서"])

        self.hbox = QHBoxLayout(self.centralWidget)

        wide = 740 / len(labels)

        for idx, item in enumerate(labels):
            item.resize(wide,30)



        self.setCentralWidget(self.centralWidget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())