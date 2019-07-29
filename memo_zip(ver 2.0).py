from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QTabWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import QDateTime, QTime, QTimer, Qt, QDate, pyqtSlot, QSize
# import cv2
# import glob
import sys
# import ctypes
import pymysql
import query


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setWindowTitle('MemoApp')
        self.message = "{0}".format(self.__datetime.toString("MM월 dd일 dddd  ap hh:mm:ss"))
        self.statusBar().showMessage(self.message)
        self.resize(879, 879)
        self.center()

    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())

class Datetime(QDateTime):
    def __init__(self, input_QDatetime=None):
        super().__init__()
        self.setCurrenDateTime()

        if input_QDatetime != None :
            self.targetDateTime = input_QDatetime

    def dateUp(self):
        self.addDays()

    def print_date(self):
        return [self.targetDateTime.date(), self.targetDateTime.date().toString("MM월 dd일 dddd")]

    def print_time(self):
        return [self.targetDateTime.time(), self.targetDateTime.time().toString("ap hh:mm")]

    def print_dateTime(self):
        return [self.targetDateTime, QDateTime.toString(self.targetDateTime,"MM월 dd일 dddd  ap hh:mm")]

    def setCurrenDateTime(self):
        self.targetDateTime = self.currentDateTime()

    def setCompleteDateTime(self):
        self.targetDateTime = self.currentDateTime()
        self.targetDateTime.setTime(QTime(17, 0, 0, 0))

    def dateUp(self):
        self.targetDateTime.addDays(1)
        return self.targetDateTime

    def dateDown(self):
        self.targetDateTime.addDays(-1)
        return self.targetDateTime

    def timeUp(self):
        self.targetDateTime.addSecs(1800)
        return self.targetDateTime

    def timeDown(self):
        self.targetDateTime.addSecs(-1800)
        return self.targetDateTime

    def isBeforeTime(self, QdateTime):
        limitDateTime = self.targetDateTime.addSecs(600)
        self.targetDateTime.addSecs(800)
        if self.targetDateTime >= QdateTime:
            if limitDateTime < self.targetDateTime:
                return 'Limited'
            else:
                return True
        else:
            return False

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # memoapp = MainWindow()
    #
    # sys.exit(app.exec_())

    dateTime = Datetime()
    dateTime.setCurrenDateTime()

    complete = Datetime()
    complete.setCompleteDateTime()
    print(dateTime.print_dateTime())
    print(complete.print_dateTime())

    dateTime1 = Datetime(complete.print_dateTime()[0])
