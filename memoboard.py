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

        self.labels = [QLabel(self.centralWidget) for i in range(6)]

        for idx,item in enumerate(self.labels):
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

        # self.textEdit = QTextEdit(self.centralWidget)
        # self.textEdit.setMaximumSize(QSize(16777215, 200))
        # self.vbox.addWidget(self.textEdit)

        self.framebox = QVBoxLayout(self.centralWidget)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()

        # labeltest = QLabel(self.centralWidget)
        # labeltest.setText("111")
        # self.vbox.addWidget(labeltest)


        wide =int( 740 / len(self.labels))


        for idx, label in enumerate(self.labels):
            # item.resize(wide,50)
            # item.move(wide*(idx)+10,10)
            label.setFixedHeight(50)
            self.hbox.addWidget(label)
            print(label.width())



        self.hbox.setSpacing(7)

        self.vbox.addLayout(self.hbox)

        spacerItem = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.vbox.addItem(spacerItem)

        label1 = QLabel(self.centralWidget)

        self.framebox.addLayout(self.vbox)

        self.setCentralWidget(self.centralWidget)


    def mousePressEvent(self, event):
        # self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        label_size = [[i.width(),i.height()] for i in self.labels]
        label_section = []
        space = 5
        buf_xpos = 0
        buf_ypos = 0

        for idx, size in enumerate(label_size):
            if idx ==0:
                buf_xstart = space
                buf_xend = size[0] + space
                buf_heigth = size[1]
                label_section.append((buf_xstart, buf_xend,buf_ypos,buf_heigth))
            else:
                buf_xstart = buf_xend
                buf_xend = size[0] + space
                buf_heigth = size[1]
                label_section.append((buf_xstart, buf_xend, buf_ypos, buf_heigth))


        self.mousePR = True
        message = "{0}     {1}     Mouse 위치 ; x={2},y={3}, global={4},{5}". \
                    format("누름",self.time.toString(Qt.DefaultLocaleLongDate), event.x(), event.y(), event.globalX(), event.globalY())
        posmee="{}".format(label_size) #self.labels[0].width())
        print(label_section)
        self.statusBar().showMessage(posmee)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())