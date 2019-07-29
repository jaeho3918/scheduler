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


class Datetime(QDateTime):
    def __init__(self, QDatetime = None):
        if QDatetime == None :
            super().__init__()
        else:
            super().__init__()
            self.targetDateTime = QDateTime

    def dateUp(self):
        self.addDays()

    def toDateTime(self):
        return {'Date' : [self.targetDateTime.date(),self.targetDateTime.date().toString("MM월 dd일 dddd")],
                'Time': [self.targetDateTime.time(), self.targetDateTime.time().toString("ap hh:mm")],
                'DateTime' : [self.targetDateTime,self.targetDateTime.toString("MM월 dd일 dddd  ap hh:mm")]}

    def setCurrenDateTime(self):
        self.targetDateTime = self.currentDateTime()

    def setCompleteDateTime(self):
        self.targetDateTime = self.currentDateTime()
        self.targetDateTime.setTime(QTime(17,0,0,0))
        # self.targetDateTime.setTime()

    def dateUp(self):
        self.targetDateTime.addDays(1)

    def dateDown(self):
        self.targetDateTime.addDays(-1)

    def timeUp(self):
        self.targetDateTime.addSecs(1800)

    def timeDown(self):
        self.targetDateTime.addSecs(-1800)

    def isBeforeTime(self, QdateTime):
        limitDateTime = self.targetDateTime.addSecs(600)
        print('!!!!!!!!!!',limitDateTime,self.targetDateTime)
        self.targetDateTime.addSecs(800)
        if self.targetDateTime >= QdateTime:
            if limitDateTime < self.targetDateTime:
                return 'Limited'
            else:
                return True
        else :
            return False










if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # memoapp = MainWindow()
    #
    # sys.exit(app.exec_())

    datetime = Datetime()
    datetime.setCurrenDateTime()

    complete = Datetime()
    complete.setCompleteDateTime()
    print(datetime.toDateTime()['Time'])
    print(complete.toDateTime()['Time'])
    print(datetime.toDateTime()['Time'][0] >complete.toDateTime()['Time'][0])
    print(datetime.isBeforeTime(complete.toDateTime()['DateTime'][0]))
    print(datetime.toDateTime()['DateTime'], complete.toDateTime()['DateTime'])

    print(complete.toDateTime()['DateTime'][0])
    datetime = Datetime(complete.toDateTime()['DateTime'][0])
    print(datetime.toDateTime()['DateTime'][0 ])
