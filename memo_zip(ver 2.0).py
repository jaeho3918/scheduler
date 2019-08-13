from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QTabWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import QDateTime, QTime, QTimer, Qt, QDate, pyqtSlot, QSize

import sys
import pymysql
import query

# import cv2
# import glob
# import ctypes


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

        if (self.date().year() % 4) == 0:
            self._month_table = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #윤년
        else :
            self._month_table = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31] #평년

        if input_QDatetime != None:
            self.targetDateTime = input_QDatetime

    def get_date(self):
        return [self.targetDateTime.date(), self.targetDateTime.date().toString("MM월 dd일 dddd")]

    def get_time(self):
        return [self.targetDateTime.time(), self.targetDateTime.time().toString("ap hh:mm")]

    def get_dateTime(self):
        return [self.targetDateTime, QDateTime.toString(self.targetDateTime, "MM월 dd일 dddd  ap hh:mm")]

    def set_currenDateTime(self):
        self.targetDateTime = self.currentDateTime()

    def set_completeDateTime(self):
        self.targetDateTime = self.currentDateTime()
        self.targetDateTime.setTime(QTime(17, 0, 0, 0))

    def increase_date(self):
        self.targetDateTime.addDays(1)
        return self.targetDateTime

    def decrease_date(self):
        self.targetDateTime.addDays(-1)
        return self.targetDateTime

    def increase_time(self):
        self.targetDateTime.addSecs(1800)
        return self.targetDateTime

    def reduce_time(self):
        self.targetDateTime.addSecs(-1800)
        return self.targetDateTime

    def compare_datetime(self, input_compdate):
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

        print(comp1_date,comp1_time, ":::",comp2_date,comp2_time)

        buf_sublist = []  # [year, month, hour, minute, second]
        buf_sublist.append(comp2_date[0] - comp1_date[0])
        buf_sublist.append(comp2_date[1] - comp1_date[1])
        buf_sublist.append(comp2_date[2] - comp1_date[2])
        buf_sublist.append(comp2_time[0] - comp1_time[0])
        buf_sublist.append(comp2_time[1] - comp1_time[1])

        minus_index = [buf_sublist.index(i) for i in buf_sublist if i < 0]

        rounding_table = [0, 0, 0, 24, 60]

        print('@@@@@@@@',minus_index)

        for i in minus_index:
            if i > 2:
                buf_sublist[i - 1] -= 1
                buf_sublist[i] += (rounding_table[i]+1)

            elif i == 2 :
                buf_sublist[i - 1] -= 1
                buf_sublist[i] += (self._month_table[comp1_date[1]]+1)


        datetime_header = ['year','month','date','hour','minute']

        result = {}

        for idx, value in enumerate(buf_sublist):
            result[datetime_header[idx]] = value

        return result



if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # memoapp = MainWindow()
    #
    # sys.exit(app.exec_())

    dateTime = Datetime()
    dateTime.set_currenDateTime()
    complete = Datetime()
    complete.setCompleteDateTime()

    compareDateTime = QDateTime()
    compareDateTime.setDate(QDate(2019, 8, 9))
    compareDateTime.setTime(QTime(14, 40, 0, 0))

    dateTime1 = Datetime(dateTime.get_dateTime()[0])
    sub_dateTime = dateTime1.compare_datetime(compareDateTime)

    for timeunit, value in sub_dateTime.items():
        print(timeunit, value)