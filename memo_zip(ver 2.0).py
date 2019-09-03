from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QTabWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import QDateTime, QTime, QTimer, Qt, QDate, pyqtSlot, QSize
from datetime import date, datetime, timedelta
import sys
import pymysql
import query
import locale

locale.setlocale(locale.LC_ALL, '')


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


class Datetime1(QDateTime):
    def __init__(self, input_QDatetime=None):
        super().__init__()
        self.set_curren_datetime()

        if (self.date().year() % 4) == 0:
            self._month_table = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 윤년
        else:
            self._month_table = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # 평년

        if input_QDatetime != None:
            self.targetDateTime = input_QDatetime

    def __str__(self):
        return f'self.targetDateTime, QDateTime.toString(self.targetDateTime, "MM월 dd일 dddd  ap hh:mm")'

    def get_date(self):
        return [self.targetDateTime.date(), self.targetDateTime.date().toString("MM월 dd일 dddd")]

    def get_time(self):
        return [self.targetDateTime.time(), self.targetDateTime.time().toString("ap hh:mm")]

    def get_dateTime(self):
        return [self.targetDateTime, QDateTime.toString(self.targetDateTime, "MM월 dd일 dddd  ap hh:mm")]

    def set_curren_datetime(self):
        self.targetDateTime = self.currentDateTime()

    def set_complete_datetime(self):
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

        print(comp1_date, comp1_time, ":::", comp2_date, comp2_time)

        buf_sublist = []  # [year, month, hour, minute, second]
        buf_sublist.append(comp2_date[0] - comp1_date[0])
        buf_sublist.append(comp2_date[1] - comp1_date[1])
        buf_sublist.append(comp2_date[2] - comp1_date[2])
        buf_sublist.append(comp2_time[0] - comp1_time[0])
        buf_sublist.append(comp2_time[1] - comp1_time[1])

        minus_index = [buf_sublist.index(i) for i in buf_sublist if i < 0]

        rounding_table = [0, 0, 0, 24, 60]

        print('@@@@@@@@', minus_index)

        for i in minus_index:
            if i > 2:
                buf_sublist[i - 1] -= 1
                buf_sublist[i] += (rounding_table[i] + 1)

            elif i == 2:
                buf_sublist[i - 1] -= 1
                buf_sublist[i] += (self._month_table[comp1_date[1]] + 1)

        datetime_header = ['year', 'month', 'date', 'hour', 'minute']

        result = {}

        for idx, value in enumerate(buf_sublist):
            result[datetime_header[idx]] = value

        return result


class Datetime(datetime):
    def __new__(cls, *args):
        return super(Datetime, cls).__new__(cls, *args)

    def __init__(self, *args):
        super().__init__()

        if not self.year % 4:
            _MONTH_TABLE = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)  # 윤년
        else:
            _MONTH_TABLE = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)  # 평년

    def __str__(self):
        return f"{self.strftime('%Y%m월 %d일(%A) %p %I시 %M분').encode().decode('UTF-8')}"

    def __repr__(self):
        return f"{self.strftime('%Y%m월 %d일(%A) %p %I시 %M분').encode().decode('UTF-8')}"

    def get_datetime(self):
        return (self.year, self.month, self.day, self.hour, self.second)

    def compare_datetime(self, compare_datetime):
        # (self.year, self.month, self.day, self.hour, self.second)
        my_datetime = (self.year,
                       self.month,
                       self.day,
                       self.hour,
                       self.second)
        compare_datetime = (compare_datetime.year,
                            compare_datetime.month,
                            compare_datetime.day,

                            compare_datetime.hour,
                            compare_datetime.second)

        return ([i - j for i, j in zip(my_datetime, compare_datetime)])

    def set_completetime(self):
        self.time(1, 1, 1)

def test ()\
        :
    print(111)

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # memoapp = MainWindow()
    #
    # sys.exit(app.exec_())

    # dateTime = Datetime()
    # dateTime.set_curren_datetime()
    # complete = Datetime()
    # complete.set_complete_datetime()
    #
    # compareDateTime = QDateTime()
    # compareDateTime.setDate(QDate(2019, 8, 9))
    # compareDateTime.setTime(QTime(14, 40, 0, 0))
    #
    # print('111111111111',compareDateTime)
    #
    # dateTime1 = Datetime(dateTime.get_dateTime()[0])
    # sub_dateTime = dateTime1.compare_datetime(compareDateTime)
    #
    # for timeunit, value in sub_dateTime.items():
    #     print(timeunit, value)

    day1 = Datetime.today()
    print(day1)

    day2 = Datetime.today()
    plus_datetime = timedelta(hours=13)
    day2 = day2 + plus_datetime

    print(day1.compare_datetime(day2))

    print(day2.set_completetime())
