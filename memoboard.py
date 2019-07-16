from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import glob
import sys
import ctypes

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.date = QDate.currentDate()
        self._year = self.date.year()
        self.date_str = self.date.toString("MM월 dd일 dddd")

        self.time = QTime.currentTime()
        self.time_str = self.time.toString("ap hh:mm")

        self.complete_date = QDate.currentDate()
        self.complete_dateforarray = self.complete_date
        self.complete_date_str = self.complete_date.toString("MM월 dd일 dddd")

        self.complete_time = QTime().currentTime()
        self.complete_time_str =self.time.toString("ap hh:mm")

        self.complete_datetime = [self.complete_date, self.complete_time]
        self.complete_datetime_str = self.complete_date_str+ ' ' + self.complete_time_str

        self.close_time = QTime()
        self.close_time.setHMS(17,00,00)
        self.close_time_str = self.close_time.toString("ap hh:mm")

        # date1 = QTime()
        # date2 = QTime()
        #
        # date1.setHMS(18, 5, 7)
        # date2.setHMS(18, 5, 7)
        #
        # print(date1==date2, date1)


        self.datetime_str = "{0} {1}".format(self.date_str, self.time_str)

        self._STATUS = 18
        self._save_table_items = []
        self._tableHeader = ["유형", "내용", "작성날짜","완결날짜", "완결", "삭제"]
        self._tablewidth = [90, 290, 173, 173, 55, 55]
        self.savetablearray = []

        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setWindowTitle('Memoboard')
        self.message = "{0} {1}".format("Ready", self.datetime_str)
        self.statusBar().showMessage(self.message)
        self.timer()

        self.resize(879, 879)
        self.center()

        self.centralWidget = QWidget(self)
        self.framebox = QVBoxLayout(self.centralWidget)

        self.status_menu()
        self.status_label_layout = QHBoxLayout()
        self.status_label()

        self.status_time_layout = QHBoxLayout()
        self.status_time()
        self.status_textedit_layout = QVBoxLayout()
        self.status_textedit()
        self._STATUS = 15
        self.status_btn()
        self.save_table()


        self.framebox.addLayout(self.status_menulayout)
        self.framebox.addLayout(self.status_label_layout)
        self.framebox.addLayout(self.status_time_layout)
        self.framebox.addLayout(self.status_textedit_layout)
        self.framebox.addLayout(self.save_btn_layout)
        self.framebox.addLayout(self.save_table_layout)
        spacerItem = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.framebox.addItem(spacerItem)

        self.setCentralWidget(self.centralWidget)
        self.show()

    def status_time(self, reset=False):

        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(7)
        font.setBold(True)

        self.timebtnvbox = QVBoxLayout()
        self.timebtnvbox.setSpacing(1)

        self.timetodaybtn = QPushButton()
        self.timetodaybtn.setFont(font)
        self.timetodaybtn.setFixedWidth(30)
        self.timetodaybtn.setFixedHeight(15)
        self.timetodaybtn.setText('▼')
        self.timetodaybtn.clicked.connect(self.timetodaybtn_clicked)


        self.timetomorrowbtn = QPushButton()
        self.timetomorrowbtn.setFont(font)
        self.timetomorrowbtn.setFixedWidth(30)
        self.timetomorrowbtn.setFixedHeight(15)
        self.timetomorrowbtn.setText('▲')
        self.timetomorrowbtn.clicked.connect(self.timetomorrowbtn_clicked)

        self.timebtnvbox.addWidget(self.timetomorrowbtn)
        self.timebtnvbox.addWidget(self.timetodaybtn)

        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(11)
        font.setBold(True)


        if reset ==False:

            self.timelabel1 = QLabel()
            self.timelabel1.setFont(font)

            self.timelabel1.setFixedWidth(300)
            self.timelabel1.setFixedHeight(30)

            self.timelabel2 = QLabel()
            self.timelabel2.setFont(font)
            self.timelabel2.setText('완결시간 :')
            self.timelabel2.setFixedWidth(71)

            self.timelinedit = QLabel()
            self.timelinedit.setFont(font)
            self.timelinedit.setFixedWidth(170)

            self.timelinedit2 = QLabel()
            self.timelinedit2.setFont(font)

            self.timelinedit2.setFixedWidth(85)

            self.status_time_layout.addWidget(self.timelabel1)
            self.status_time_layout.addStretch(2)
            self.status_time_layout.addWidget(self.timelabel2)
            self.status_time_layout.addWidget(self.timelinedit)
            self.status_time_layout.addLayout(self.timebtnvbox)
            self.status_time_layout.addWidget(self.timelinedit2)

        complete_date_str = self.complete_date.toString(("MM월 dd일 dddd"))
        self.timelabel1.setText('오늘날짜 : {}'.format(self.datetime_str))
        self.timelinedit.setAlignment(Qt.AlignCenter)
        self.timelinedit.setText('{}'.format(self.complete_date_str))
        self.timelinedit2.setText(QTime.toString(self.close_time,"ap hh:mm"))
        self.status_time_layout.update()

    def changeclosetime(self):
        buf_str = self.close_time.fromString(self.timelinedit2.text(),"ap hh:mm")
        self.close_time_str = QTime.toString(buf_str,"ap hh:mm")

    def changeclosedate(self):
        buf_str = self.timelinedit.text()
        print(self.complete_date.year(), buf_str.split("월 ")[0][-3:],  buf_str.split("월 ")[1].split("일 ")[0])

        buf_str = self.complete_date.setDate(self.complete_date.year(),
                                             int(buf_str.split("월 ")[0][-3:]),
                                             int(buf_str.split("월 ")[1].split("일 ")[0]))

        self.complete_date_str = QDate.toString(self.complete_date,"MM월 dd일 dddd")

        self.timelinedit.setText('{}'.format(self.complete_date_str))

        # print(self.complete_date_str)

    def timetodaybtn_clicked(self):
        self.complete_datebtn = self.date
        buf_day = [self.complete_date.year(), self.complete_date.month(), self.complete_date.day()]
        if (buf_day[2]-1)!=0:
            self.complete_date.setDate(buf_day[0],buf_day[1], buf_day[2]-1)
            self.complete_dateforarray = self.complete_date
        else:
            self.complete_date = self.date

        complete_date_str = self.complete_date.toString("MM월 dd일 dddd")

        buf_str = QDate.fromString(complete_date_str,"MM월 dd일 dddd")
        buf_str.setDate(self.complete_dateforarray.year(), buf_str.month(),buf_str.day())

        self.complete_time = self.close_time
        complete_time_str= self.complete_time.toString("ap hh:mm")

        self.complete_datetime = [self.complete_date, self.complete_time]
        self.complete_datetime_strbtn = complete_date_str

        self.timelinedit.setText('{}'.format(self.complete_datetime_strbtn))




    def timetomorrowbtn_clicked(self):

        self.complete_date = self.date
        self.complete_date = self.complete_date.addDays(1)
        self.complete_dateforarray = self.complete_date
        self.complete_date_str = self.complete_date.toString(("MM월 dd일 dddd"))

        self.complete_time = self.close_time

        self.complete_datetime = [self.complete_date, self.complete_time]
        self.complete_time_str= self.complete_time.toString("ap hh:mm")

        self.complete_datetime_strbtn = self.complete_date_str

        self.timelinedit.setText('{}'.format(self.complete_datetime_strbtn))



    def reset_time(self):
        self.date = QDate.currentDate()
        self.complete_date = self.date
        self.complete_date_str = self.complete_date.toString(("MM월 dd일 dddd"))

        self.complete_time = self.close_time
        self.complete_time_str = self.complete_time.toString("ap hh:mm")

        self.complete_datetime = [self.complete_date, self.complete_time]
        self.complete_datetime_str = self.complete_date_str + ' ' + self.complete_time_str


    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())

    def updatetime_alram(self):
        self.time = QTime.currentTime()
        self.time_str = self.time.toString("ap hh:mm")
        self.datetime_str = "{0} {1}".format(self.date_str, self.time_str)
        self.message = "{0} {1}".format("Ready", self.datetime_str)
        self.statusBar().showMessage(self.message)


        # print(0,0,":",self.saveTable.rowCount(), self.saveTable.cellWidget(0,0))

        for i in range(self.saveTable.rowCount()):
            for j in range(6):
                if j == 3:
                    buf_widget = self.saveTable.cellWidget(i,j)
                    print(id(buf_widget))


                    # if self.saveTable.setCellWidget(i,3) <= self.date:
                    #     print('뀨뀨뀨뀨뀨뀨뀨!!!!!!!!!!!!!!!!!!!!',i)

    def timer(self):
        self.Qtimer = QTimer()
        self.Qtimer.timeout.connect(self.updatetime_alram)
        self.Qtimer.start(1000)

    def status_menu(self, reset =True):

        self.status = ["대사관", "아포스티유", "공증", "등기", "견적서", "계산서"]
        self.status_stylesheet = {"대사관": "color: black;"  # 빨간색
                                         "background-color: #abd1ff;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #7EB9FF;"
                                         "border-radius: 8px",
                                  "아포스티유": "color: black;"  # 주황색
                                           "background-color: #fcb77e;"
                                           "border-style: solid;"
                                           "border-width: 3px;"
                                           "border-color: #fc9d4e;"
                                           "border-radius: 8px",
                                  "공증": "color: black;"  # 초록색
                                        "background-color: #cfeb8a;"
                                        "border-style: solid;"
                                        "border-width: 3px;"
                                        "border-color: #b3eb2b;"
                                        "border-radius: 8px",
                                  "등기": "color: black;"  # 보라색
                                        "background-color: #e3c4ff;"
                                        "border-style: solid;"
                                        "border-width: 3px;"
                                        "border-color: #C486FF;"
                                        "border-radius: 8px",
                                  "견적서": "color: black;"  # 노란색
                                         "background-color: #ffffb8;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #FEFF7F;"
                                         "border-radius: 8px",
                                  "계산서": "color: black;"  # 노란색
                                         "background-color: #ffffb8;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #FEFF7F;"
                                         "border-radius: 8px"
                                  }
        self.status_stylesheet1 = {"대사관": QColor(171,209,255),
                                  "아포스티유": QColor(252,183,126),
                                  "공증": QColor(207,235,138),
                                  "등기": QColor(227,196,255),
                                  "견적서": QColor(255,255,184),
                                  "계산서": QColor(255,255,184)
                                  }

        self.labels = [QLabel(self.centralWidget) for _ in range(6)]

        for idx, item in enumerate(self.labels):
            font = QFont()
            font.setFamily("맑은 고딕")
            font.setPointSize(18)
            font.setBold(True)

            item.setFont(font)
            item.setStyleSheet(self.status_stylesheet[self.status[idx]])
            item.setText("{}".format(self.status[idx]))
            item.setAlignment(Qt.AlignCenter)

        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(7)

        for idx, label in enumerate(self.labels):
            # item.resize(wide,50)
            # item.move(wide*(idx)+10,10)
            label.setFixedHeight(50)
            self.hbox.addWidget(label)
            #print(label.width())

        self.status_menulayout = QVBoxLayout()
        self.status_menulayout.addLayout(self.hbox)

    def status_label(self):

        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)
        self.normal_stylesheet = {"normal": "color: gray;"
                                            "border-style: solid;"
                                            "border-width: 2px;"
                                            "border-color: gray;"
                                            "border-radius: 3px"}

        if 0 <= self._STATUS <= len(self.labels):
            self.statusLabel.deleteLater()
            self.statusLabel = None
            self.statusLabel = QLabel(self.centralWidget)
            self.statusLabel.setFont(font)
            self.statusLabel.setStyleSheet(self.status_stylesheet[self.status[self._STATUS]])
            self.statusLabel.setText("유 형 : {}".format(self.status[self._STATUS]))
            self.statusLabel.setAlignment(Qt.AlignLeft)
            self.status_label_layout.addWidget(self.statusLabel)

        else:
            if self._STATUS == 15:
                self.statusLabel.deleteLater()
                self.statusLabel = None
                self.statusLabel = QLabel(self.centralWidget)
                self.statusLabel.setFont(font)
                self.statusLabel.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusLabel.setText("유 형 : 선택해주세요.")
                self.statusLabel.setAlignment(Qt.AlignLeft)
                self.status_label_layout.addWidget(self.statusLabel)

            elif self._STATUS == 18:
                self.statusLabel = QLabel(self.centralWidget)
                self.statusLabel.setFont(font)
                self.statusLabel.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusLabel.setText("유 형 : 선택해주세요.")
                self.statusLabel.setAlignment(Qt.AlignLeft)
                self.status_label_layout.addWidget(self.statusLabel)

            self._STATUS == 15



        self.status_label_layout.update()

    def status_textedit(self):
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        font.setBold(False)

        if 0 <= self._STATUS <= len(self.labels):
            self.statusTextedit.deleteLater()
            self.statusTextedit = None
            self.statusTextedit = QTextEdit(self.centralWidget)
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(self.status_stylesheet[self.status[self._STATUS]])
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.status_textedit_layout.addWidget(self.statusTextedit)
        else:
            if self._STATUS == 15:
                self.statusTextedit.deleteLater()
                self.statusTextedit = None
                self.statusTextedit = QTextEdit(self.centralWidget)
                self.statusTextedit.setFont(font)
                self.statusTextedit.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
                self.statusTextedit.setAlignment(Qt.AlignLeft)
                self.status_textedit_layout.addWidget(self.statusTextedit)

            elif self._STATUS == 18:
                self.statusTextedit = QTextEdit(self.centralWidget)
                self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
                self.statusTextedit.setFont(font)
                self.statusTextedit.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusTextedit.setAlignment(Qt.AlignLeft)
                self.status_textedit_layout.addWidget(self.statusTextedit)

            self._STATUS == 15

        self.status_textedit_layout.update()

    def status_btn(self):
        self.save_btn_layout = QVBoxLayout()
        self.save_btn = QPushButton()
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)
        self.save_btn.setText('입력')
        self.save_btn.setFixedHeight(50)
        self.save_btn.setFont(font)
        self.save_btn.clicked.connect(self.save_btn_clicked)
        self.save_btn_layout.addWidget(self.save_btn)
        self.save_btn_layout.update()

    def save_table(self):
        self.SAVE_TABLE_COUNT = 0
        self.save_table_layout = QVBoxLayout()

        self.saveTable = QTableWidget(self.centralWidget)
        self.saveTable.setLineWidth(1)
        self.saveTable.setObjectName("tableWidget")
        self.saveTable.setColumnCount(6)
        self.saveTable.setHorizontalHeaderLabels(self._tableHeader)
        settablewidth = [self.saveTable.setColumnWidth(idx, width)
                         for idx, width in enumerate(self._tablewidth)]

        self.save_table_layout.addWidget(self.saveTable)
        self.save_table_layout.update()

    def mousePressEvent(self, event):
        self.pos1 = [0, 0]
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        buf_STATUS = self._STATUS
        label_size = [[i.width(), i.height()] for i in self.labels]
        label_section = []
        space = 5
        buf_xpos = 0
        buf_ypos = 0

        for idx, size in enumerate(label_size):
            if idx == 0:
                buf_xstart = space
                buf_xend = size[0] + space
                buf_heigth = size[1]
                label_section.append((buf_xstart, buf_xend, buf_ypos, buf_heigth))
            else:
                buf_xstart = buf_xend + space
                buf_xend = buf_xstart + size[0]
                buf_heigth = size[1]
                label_section.append((buf_xstart, buf_xend, buf_ypos, buf_heigth))

        self.mousePR = True

        for idx, section in enumerate(label_section):
            if section[0] <= self.pos1[0] <= section[1]:
                if section[2] <= self.pos1[1] <= section[3]:
                    print(self.status[idx])
                    self._STATUS = idx

        # if buf_STATUS == self._STATUS:
        #     self._STATUS = 15

        self.status_label()
        self.status_textedit()
        self.update()

    def save_btn_clicked(self):
        statusTextedit = self.statusTextedit.toPlainText()
        if not (0 <= self._STATUS <= len(self.status)) \
                or (len(statusTextedit) == 0):
            self.save_btn.setText("유형을 선택해주세요.")
            if not (0 <= self._STATUS <= len(self.status)):
                self.save_btn.setText("유형을 선택해주세요.")
            elif len(statusTextedit) == 0:
                self.save_btn.setText("내용을 입력해주세요.")
        else:
            self.save_btn.setText("입력")


            timeforarray = QTime.fromString(self.timelinedit2.text(),"ap hh:mm")

            self.save_table_additems = [self.status[self._STATUS],
                                        statusTextedit,
                                        self.datetime_str,
                                        self.complete_datetime_str,
                                        "완결",
                                        "삭제"]

            self.save_table_additemsforarray = [self.status[self._STATUS],
                                        statusTextedit,
                                        self.datetime_str,
                                        [self.complete_dateforarray,timeforarray],
                                        "완결",
                                        "삭제"]

            self.savetablearray.append(self.save_table_additemsforarray) ######여기

            self.SAVE_TABLE_COUNT += 1

            # print(self.SAVE_TABLE_COUNT, self.save_table_additems)

            self.saveTable.setRowCount(self.SAVE_TABLE_COUNT)

            buf_labels = []

            for idx, item in enumerate(self.save_table_additems):
                if idx<=2:
                    brush = QBrush(self.status_stylesheet1[self.status[self._STATUS]])
                    brush.setStyle(Qt.SolidPattern)

                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(item)
                    setitem.setTextAlignment(Qt.AlignCenter)

                    buf_item = self.saveTable.setItem(self.SAVE_TABLE_COUNT - 1, idx, setitem)

                    # buf_item.setStyleSheet(self.status_stylesheet1[self.status[self._STATUS]][:-19])
                    # buf_item.setAlignment(Qt.AlignCenter)


                if idx == 3:
                    brush = QBrush(self.status_stylesheet1[self.status[self._STATUS]])
                    brush.setStyle(Qt.SolidPattern)

                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(item)
                    setitem.setTextAlignment(Qt.AlignCenter)

                    buf_item = self.saveTable.setItem(self.SAVE_TABLE_COUNT - 1, idx, setitem)

                elif idx == 4:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(item)
                    buf_item.setFixedWidth(self._tablewidth[idx])
                    buf_item.setStyleSheet(self.edit_stylesheet(self.status[self._STATUS],
                                                                color=True,
                                                                background_color=True,
                                                                border_color=False,
                                                                border_radius=False,
                                                                border_width=False,
                                                                border_style=False))
                    self.saveTable.setCellWidget(self.SAVE_TABLE_COUNT - 1, idx, buf_item)

                elif idx == 5:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(item)
                    buf_item.setFixedWidth(self._tablewidth[idx])
                    buf_item.setStyleSheet(self.edit_stylesheet(self.status[self._STATUS],
                                             color=True,
                                             background_color=True,

                                             border_color=False,
                                             border_radius=False,
                                             border_width=False,
                                             border_style=False))
                    self.saveTable.setCellWidget(self.SAVE_TABLE_COUNT - 1, idx, buf_item)

                buf_labels.append(buf_item)

            self._STATUS = 15
            self._save_table_items.append(buf_labels)
            self.status_label()
            self.reset_data()
            self.update()


    def reset_data(self):
        # self.status_label()
        self.status_textedit()
        self.status_time(reset=True)
        self.status_time(reset=True)

    def addtable_labels(self,str_array):
        buf_labels =[]
        for string in str_array:
            buf_item = QLabel(self.centralWidget)
            buf_item.setText(string)
            buf_item.setStyleSheet(self.status_stylesheet[self.status[self._STATUS]][:-19])
            buf_item.setAlignment(Qt.AlignCenter)
            buf_labels.append(buf_item)

        return buf_labels

    def edit_stylesheet(self,
                        status,
                        color=True,
                        background_color=True,
                        border_style =True,
                        border_width =True,
                        border_color = True,
                        border_radius = True):
        buf_string = ""
        stylesheet = {"대사관": ["black;",  # 빨간색
                            "#abd1ff;",
                            "solid;",
                            "3px;",
                            "#7EB9FF;",
                            "8px"],
                 "아포스티유": ["black;",  # 주황색
                          "#fcb77e;",
                          "solid;",
                          "3px;",
                          "#fc9d4e;",
                          "8px"],
                 "공증": ["black;",  # 초록색
                           "#cfeb8a;",
                           "solid;",
                           "3px;",
                           "#b3eb2b;",
                           "8px"],
                 "등기": ["black;",  # 보라색
                           "#e3c4ff;",
                           "solid;",
                           "3px;",
                           "#C486FF;",
                           "8px"],
                 "견적서": ["black;",  # 노란색
                            "#ffffb8;",
                            ": solid;",
                            "3px;",
                            "#FEFF7F;",
                            "8px"],
                 "계산서": ["black;",  # 노란색
                            "#ffffb8;",
                            "solid;",
                            "3px;",
                            "#FEFF7F;",
                            "8px"]
                 }
        if color == True :
            buf_string = buf_string + "color: " + stylesheet[status][0]  # 빨간색
        if background_color == True:
            buf_string = buf_string + "background-color: " + stylesheet[status][1]
        if border_style == True:
            buf_string = buf_string + "border-style: " + stylesheet[status][2]
        if border_width == True:
            buf_string = buf_string + "border-width: " + stylesheet[status][3]
        if border_color == True:
            buf_string = buf_string + "border-color: " + stylesheet[status][4]
        if border_radius == True:
            buf_string = buf_string + "border-radius: " + stylesheet[status][5]

        return buf_string



if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())