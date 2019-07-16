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

        self.__STATUS = 18 # 대사관:0, 아포:1, 공증:2, 등기:3, 견적서:4, 계산서:5  첫번째 생성: 18, 두번째 셋팅:15
        self.__statusList = ["대사관", "아포스티유", "공증", "등기", "견적서", "계산서"]
        self.__datetime = QDateTime.currentDateTime()
        self.__completeDatetime = QDateTime.currentDateTime()
        buf_time = QTime()
        buf_time.setHMS(17,0,0)
        self.__completeDatetime.setTime(buf_time)

        self.__save_table_items = []
        self.__tableHeader = ["유형", "내용", "작성날짜","완결날짜", "완결", "삭제"]
        self.__tablewidth = [90, 290, 173, 173, 55, 55]
        self.__savetablearray = []
        self.__SAVE_TABLE_COUNT = 0

        self.initUI()

    def initUI(self):
        self.setWindowTitle('MemoApp')
        self.message = "{0}".format(self.__datetime.toString("MM월 dd일 dddd  ap hh:mm"))
        self.statusBar().showMessage(self.message)
        self.resize(879, 879)
        self.center()
        self.centralWidget = QWidget(self)
        self.frameLayout = QVBoxLayout(self.centralWidget)



######## setLayout
        self.menuLayout = QHBoxLayout()
        self.menuLayout.setSpacing(7)
        self.displayLayout = QVBoxLayout()
        self.timeLayout = QHBoxLayout()
        self.contentsLayout = QVBoxLayout()



######## setfunc
        self.statusMenu()
        self.statusDisplay()
        self.statusTime()
        self.statusContents()
        self.statusList()
        self.statusSummit()



######## addLayout to frame
        self.frameLayout.addLayout(self.menuLayout)
        self.frameLayout.addLayout(self.displayLayout)
        self.frameLayout.addLayout(self.timeLayout)
        self.frameLayout.addLayout(self.contentsLayout)
        self.frameLayout.addWidget(self.listTable)
        self.frameLayout.addWidget(self.summitBtn)



        self.setCentralWidget(self.centralWidget)
        self.show()


    def statusMenu(self):

        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)

        styleSheet = self.edit_stylesheet()

        self.statusMenu_layout = QVBoxLayout()
        self.statusLabels = [QLabel() for _ in range(6)]

        for idx, label in enumerate(self.statusLabels):
            label.setFont(font)
            label.setStyleSheet(styleSheet[self.__statusList[idx]])
            label.setText(self.__statusList[idx])
            label.setAlignment(Qt.AlignCenter)
            label.setFixedHeight(50)

        for label in self.statusLabels:
            self.menuLayout.addWidget(label)

    def statusDisplay(self, reset = False):
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)

        stylesheet = self.edit_stylesheet()

        if reset == True:
            self.__STATUS == 15

        if 0 <= self.__STATUS <= len(self.statusLabels):
            self.statusLabel.deleteLater()
            self.statusLabel = None
            self.statusLabel = QLabel()
            self.statusLabel.setFont(font)
            self.statusLabel.setStyleSheet(stylesheet[self.__statusList[self.__STATUS]])
            self.statusLabel.setText("유 형 : {}".format(self.__statusList[self.__STATUS]))
            self.statusLabel.setAlignment(Qt.AlignLeft)
            self.displayLayout.addWidget(self.statusLabel)

        elif self.__STATUS == 15:
            self.statusLabel.deleteLater()
            self.statusLabel = None
            self.statusLabel = QLabel()
            self.statusLabel.setFont(font)
            self.statusLabel.setStyleSheet(stylesheet['보통'])
            self.statusLabel.setText("유 형 : 선택해주세요.")
            self.statusLabel.setAlignment(Qt.AlignLeft)
            self.displayLayout.addWidget(self.statusLabel)

        elif self.__STATUS == 18:
            self.statusLabel = QLabel()
            self.statusLabel.setFont(font)
            self.statusLabel.setStyleSheet(stylesheet['보통'])
            self.statusLabel.setText("유 형 : 선택해주세요.")
            self.statusLabel.setAlignment(Qt.AlignLeft)
            self.displayLayout.addWidget(self.statusLabel)
            self.__STATUS == 15

        self.displayLayout.update()

    def statusContents(self, reset = False):
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        font.setBold(False)

        stylesheet = self.edit_stylesheet()

        if reset == True:
            self.__STATUS == 15

        if 0 <= self.__STATUS <= len(self.statusLabels):
            self.statusTextedit.deleteLater()
            self.statusTextedit = None
            self.statusTextedit = QTextEdit()
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(stylesheet[self.__statusList[self.__STATUS]])
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.contentsLayout.addWidget(self.statusTextedit)

        elif self.__STATUS == 15:
            self.statusTextedit.deleteLater()
            self.statusTextedit = None
            self.statusTextedit = QTextEdit()
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(stylesheet['보통'])
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.contentsLayout.addWidget(self.statusTextedit)

        elif self.__STATUS == 18:
            self.statusTextedit = QTextEdit()
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(stylesheet['보통'])
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.contentsLayout.addWidget(self.statusTextedit)
            self.__STATUS == 15

        self.contentsLayout.update()

    def statusTime(self, reset=False):

        if reset == False:
            font = QFont()
            font.setFamily("맑은 고딕")
            font.setPointSize(7)
            font.setBold(True)

            self.dateBtnLayout = QVBoxLayout()
            self.dateBtnLayout.setSpacing(1)

            self.upDateBtn = QPushButton()
            self.upDateBtn.setFont(font)
            self.upDateBtn.setFixedWidth(30)
            self.upDateBtn.setFixedHeight(15)
            self.upDateBtn.setText('▲')
            self.upDateBtn.clicked.connect(self.upDateBtn_clicked)

            self.downDateBtn = QPushButton()
            self.downDateBtn.setFont(font)
            self.downDateBtn.setFixedWidth(30)
            self.downDateBtn.setFixedHeight(15)
            self.downDateBtn.setText('▼')
            self.downDateBtn.clicked.connect(self.downDateBtn_clicked)

            self.dateBtnLayout.addWidget(self.upDateBtn)
            self.dateBtnLayout.addWidget(self.downDateBtn)

            self.timeBtnLayout = QVBoxLayout()
            self.timeBtnLayout.setSpacing(1)

            self.upTimeBtn = QPushButton()
            self.upTimeBtn.setFont(font)
            self.upTimeBtn.setFixedWidth(30)
            self.upTimeBtn.setFixedHeight(15)
            self.upTimeBtn.setText('▲')
            self.upTimeBtn.clicked.connect(self.upTimeBtn_clicked)

            self.downTimeBtn = QPushButton()
            self.downTimeBtn.setFont(font)
            self.downTimeBtn.setFixedWidth(30)
            self.downTimeBtn.setFixedHeight(15)
            self.downTimeBtn.setText('▼')
            self.downTimeBtn.clicked.connect(self.downTimeBtn_clicked)

            self.timeBtnLayout.addWidget(self.upTimeBtn)
            self.timeBtnLayout.addWidget(self.downTimeBtn)

            font = QFont()
            font.setFamily("맑은 고딕")
            font.setPointSize(11)
            font.setBold(True)

            self.currentDatetime = QLabel()
            self.currentDatetime.setFont(font)
            self.currentDatetime.setFixedWidth(300)
            self.currentDatetime.setFixedHeight(30)

            self.complteDatetime = QLabel()
            self.complteDatetime.setFont(font)
            self.complteDatetime.setText('완결시간 :')
            self.complteDatetime.setFixedWidth(71)

            self.completeDateLabel = QLabel()
            self.completeDateLabel.setFont(font)
            self.completeDateLabel.setFixedWidth(130)

            self.completeTimeLabel = QLabel()
            self.completeTimeLabel.setFont(font)

            self.completeTimeLabel.setFixedWidth(85)

            self.timeLayout.addWidget(self.currentDatetime)
            self.timeLayout.addStretch(2)
            self.timeLayout.addWidget(self.complteDatetime)
            self.timeLayout.addWidget(self.completeDateLabel)
            self.timeLayout.addLayout(self.dateBtnLayout)
            self.timeLayout.addWidget(self.completeTimeLabel)
            self.timeLayout.addLayout(self.timeBtnLayout)

        completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
        completeTime = self.__completeDatetime.toString("ap hh:mm")

        self.currentDatetime.setText('오늘날짜 : {}'.format(self.__datetime.toString("MM월 dd일 dddd  ap hh:mm")))
        self.currentDatetime.setAlignment(Qt.AlignCenter)

        self.completeDateLabel.setText(completeDate)
        self.completeTimeLabel.setText(completeTime)

        self.timeLayout.update()

    def upDateBtn_clicked(self):
        self.__completeDatetime = self.__completeDatetime.addDays(1)
        completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
        self.completeDateLabel.setText(completeDate)
        self.timeLayout.update()

    def downDateBtn_clicked(self):
        if self.__datetime < self.__completeDatetime :
            self.__completeDatetime = self.__completeDatetime.addDays(-1)
            completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
            self.completeDateLabel.setText(completeDate)
            self.timeLayout.update()

    def upTimeBtn_clicked(self):
        self.__completeDatetime = self.__completeDatetime.addSecs(1800)
        completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
        completeTime = self.__completeDatetime.toString("ap hh:mm")
        self.completeDateLabel.setText(completeDate)
        self.completeTimeLabel.setText(completeTime)
        self.timeLayout.update()

    def downTimeBtn_clicked(self):
        self.__completeDatetime = self.__completeDatetime.addSecs(-1800)
        completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
        completeTime = self.__completeDatetime.toString("ap hh:mm")
        self.completeDateLabel.setText(completeDate)
        self.completeTimeLabel.setText(completeTime)
        self.timeLayout.update()

    def statusList(self):


        self.listTable = QTableWidget(self.centralWidget)
        self.listTable.setLineWidth(1)
        self.listTable.setObjectName("tableWidget")
        self.listTable.setColumnCount(6)
        self.listTable.setHorizontalHeaderLabels(self.__tableHeader)
        _ = [self.listTable.setColumnWidth(idx, width)
             for idx, width in enumerate(self.__tablewidth)]

    def statusSummit(self):
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)
        self.summitBtn = QPushButton()
        self.summitBtn.setText('입력')
        self.summitBtn.setFixedHeight(50)
        self.summitBtn.setFont(font)
        self.summitBtn.clicked.connect(self.summitBtn_clicked)

    def summitBtn_clicked(self):
        statusContents = self.statusTextedit.toPlainText()
        if not (0 <= self.__STATUS <= len(self.__statusList)) \
                or (len(statusContents) == 0):
            self.summitBtn.setText("유형을 선택해주세요.")
            if not (0 <= self.__STATUS <= len(self.__statusList)):
                self.summitBtn.setText("유형을 선택해주세요.")
                return 0
            elif len(statusContents) == 0:
                self.summitBtn.setText("내용을 입력해주세요.")
                return 0
        else:
            self.summitBtn.setText("입력")

            brushColor = self.edit_stylesheet(type="brushColor")
            brush = QBrush(brushColor[self.__statusList[self.__STATUS]])
            brush.setStyle(Qt.SolidPattern)
            styleSheet = self.edit_stylesheet(color=True,
                                              background_color=True,
                                              border_color=False,
                                              border_radius=False,
                                              border_width=False,
                                              border_style=False)

            self.rowItem = [self.__statusList[self.__STATUS],
                                        statusContents,
                                        self.__datetime.toString("MM월 dd일 dddd  ap hh:mm"),
                                        self.__completeDatetime.toString("MM월 dd일 dddd  ap hh:mm"),
                                        "완결",
                                        "삭제"]

            self.__SAVE_TABLE_COUNT += 1

            self.listTable.setRowCount(self.__SAVE_TABLE_COUNT)

            buf_labels = []

            for idx, item in enumerate(self.rowItem):
                if idx <= 2:
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(item)
                    setitem.setTextAlignment(Qt.AlignCenter)
                    buf_item = self.listTable.setItem(self.__SAVE_TABLE_COUNT - 1, idx, setitem)

                if idx == 3:
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(item)
                    setitem.setTextAlignment(Qt.AlignCenter)
                    buf_item = self.listTable.setItem(self.__SAVE_TABLE_COUNT - 1, idx, setitem)

                elif idx == 4:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(item)
                    buf_item.setFixedWidth(self.__tablewidth[idx])
                    buf_item.setStyleSheet(styleSheet[self.__statusList[self.__STATUS]])
                    self.listTable.setCellWidget(self.__SAVE_TABLE_COUNT - 1, idx, buf_item)

                elif idx == 5:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(item)
                    buf_item.setFixedWidth(self.__tablewidth[idx])
                    buf_item.setStyleSheet(styleSheet[self.__statusList[self.__STATUS]])
                    self.listTable.setCellWidget(self.__SAVE_TABLE_COUNT - 1, idx, buf_item)

                buf_labels.append(buf_item)

            self.resetTool(save_event=True)
            self.update()

    def timer(self):
        self.Qtimer = QTimer()
        self.Qtimer.timeout.connect(self.updatetime_alram)
        self.Qtimer.start(1000)

    def mousePressEvent(self, event):
        self.position = [0, 0]
        self.position[0], self.position[1] = event.pos().x(), event.pos().y()

        label_size = [[i.width(), i.height()] for i in self.statusLabels]
        label_section = []
        space = 5

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
            if section[0] <= self.position[0] <= section[1]:
                if section[2] <= self.position[1] <= section[3]:
                    self.__STATUS = idx
                else:
                    self.__STATUS = 15

        self.resetTool(mouse_event=True)
        self.update()

    def resetTool(self,
                  mouse_event = False,
                  save_event = False,
                  time_event = False):

        if mouse_event == True:
            self.statusDisplay(reset=True)
            self.statusContents(reset=True)

        elif save_event == True:
            self.__STATUS = 15
            self.statusDisplay(reset=True)
            self.statusContents(reset=True)
            self.__completeDatetime = QDateTime.currentDateTime()
            buf_time = QTime()
            buf_time.setHMS(17, 0, 0)
            self.__completeDatetime.setTime(buf_time)
            self.statusTime(reset=True)

        elif time_event == True:
            self.statusDisplay(reset=True)
            self.statusContents(reset=True)


    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())

    def edit_stylesheet(self,
                        color=True,
                        background_color=True,
                        border_style =True,
                        border_width =True,
                        border_color = True,
                        border_radius = True,
                        type="styleSheet"):

        menuList = ["대사관", "아포스티유", "공증", "등기", "견적서", "계산서", "보통"]
        buf_string = ""
        buf_dic = {}
        stylesheet = {  "대사관": ["black;",  # 빨간색
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
                                    "solid;",
                                    "3px;",
                                    "#e3e472;",
                                    "8px"],
                         "계산서": ["black;",  # 노란색
                                    "#ffffb8;",
                                    "solid;",
                                    "3px;",
                                    "#e3e472;",
                                    "8px"],
                         "보통": ["gray;",
                                    "#dadada",
                                    "solid;",
                                    "2px;",
                                    "#dadada",
                                    "3px"]
                         }


        for list in menuList:
            if color == True :
                buf_string = buf_string + "color: " + stylesheet[list][0]  # 빨간색
            if background_color == True:
                buf_string = buf_string + "background-color: " + stylesheet[list][1]
            if border_style == True:
                buf_string = buf_string + "border-style: " + stylesheet[list][2]
            if border_width == True:
                buf_string = buf_string + "border-width: " + stylesheet[list][3]
            if border_color == True:
                buf_string = buf_string + "border-color: " + stylesheet[list][4]
            if border_radius == True:
                buf_string = buf_string + "border-radius: " + stylesheet[list][5]

            buf_dic[list] = buf_string
            buf_string = ""






        brushColor = {"대사관": QColor(171, 209, 255),
               "아포스티유": QColor(252, 183, 126),
               "공증": QColor(207, 235, 138),
               "등기": QColor(227, 196, 255),
               "견적서": QColor(255, 255, 184),
               "계산서": QColor(255, 255, 184)
               }

        if type == "styleSheet" :
            return buf_dic
        elif type =="brushColor":
            return brushColor

if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())