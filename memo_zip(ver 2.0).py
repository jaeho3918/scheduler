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

    def isBeforeTime(self, input_compdate):
        input_compdate = input_compdate

        comp1_date = [self.targetDateTime.date().year(),
                          self.targetDateTime.date().month(),
                          self.targetDateTime.date().day()]
        comp2_date = [input_compdate.date().year(),
                          input_compdate.date().month(),
                          input_compdate.date().day()]

        comp1_time = [self.targetDateTime.time().hour(),
                          self.targetDateTime.time().minute(),
                          self.targetDateTime.time().second()]
        comp2_time = [input_compdate.time().hour(),
                          input_compdate.time().minute(),
                          input_compdate.time().second()]

        print(comp1_date, comp1_time, comp2_date, comp2_time)
        buf_result = {}

        if comp1_time[1] != comp2_time[1]: buf_result['minute'] = comp2_time[1] - comp1_time[1]
        if comp1_time[0] != comp2_time[0]: buf_result['hour'] = comp2_time[0] - comp1_time[0]
        if comp1_date[2] != comp2_date[2]: buf_result['date'] = comp2_date[2] - comp1_date[2]
        if comp1_date[1] != comp2_date[1]: buf_result['month'] = comp2_date[1] - comp1_date[1]
        if comp1_date[0] != comp2_date[0]: buf_result['year'] = comp2_date[0] - comp1_date[0]

        print(buf_result.items())
        print(buf_result.keys())


        for i in buf_result.keys():
            print(i, buf_result[i])


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # memoapp = MainWindow()
    #
    # sys.exit(app.exec_())

    dateTime = Datetime()
    dateTime.setCurrenDateTime()

    complete = Datetime()
    complete.setCompleteDateTime()

    compareDateTime = QDateTime()
    compareDateTime.setDate(QDate(2019,7,31))
    compareDateTime.setTime(QTime(17, 0, 0, 0))

    dateTime1 = Datetime(dateTime.print_dateTime()[0])
    dateTime1.isBeforeTime(compareDateTime)
