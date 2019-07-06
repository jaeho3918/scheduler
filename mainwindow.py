# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore,  QtWidgets
from PyQt5.QtGui import QPainter, QColor
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(430, 110, 272, 183))
        self.calendarWidget.setObjectName("calendarWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(460, 400, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(430, 40, 81, 16))
        self.checkBox.setObjectName("checkBox")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(430, 310, 271, 71))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)



        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.label(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.center(MainWindow)

    def label(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 180, 56, 12))
        self.label.setObjectName("라벨테스트@@@@@@@@@")
        self.label.setText(_translate("MainWindow", "라벨테스트@@@@@@@@@"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.checkBox.setText(_translate("MainWindow", "CheckBox"))

    def mousePressEvent(self, MainWindow):
        self.pos1[0], self.pos1[1] = MainWindow.event.pos().x(), MainWindow.event.pos().y()
        self.mousePR = True
        self.update()

    def mouseReleaseEvent(self, MainWindow):
        self.pos1[0], self.pos1[1] = MainWindow.event.pos().x(), MainWindow.event.pos().y()
        self.mousePR = False
        self.update()

    def paintEvent(self):
        if self.pos1 != [0, 0]:
            qp = QPainter()
            qp.begin(self)
            self.drawRectangles(qp)
            qp.end()

    def drawRectangles(self,qp):
        if self.mousePR ==True:
            col = QColor(0, 0, 0)
            col.setNamedColor('#d4d4d4')
            qp.setPen(col)

            qp.setBrush(QColor(200, 0, 0))
            qp.drawRect(self.pos1[0], self.pos1[1], 90, 30)

            qp.setBrush(QColor(255, 80, 0, 160))
            qp.drawRect(self.pos1[0]+110, self.pos1[1], 90, 30)

            qp.setBrush(QColor(25, 0, 90, 200))
            qp.drawRect(self.pos1[0]+220, self.pos1[1], 90, 30)
        else:
            qp.eraseRect(self.pos1[0], self.pos1[1], 500, 40)

    def center(self, MainWindow):
        framePos = MainWindow.frameGeometry()
        centerPos = QtWidgets.QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        MainWindow.move(framePos.topLeft())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
