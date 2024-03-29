from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton, QTableWidget, \
    QTableWidgetItem, QLabel, QTabWidget, QApplication, QDesktopWidget, QMessageBox
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtCore import QDateTime, QTime, QTimer, Qt, QDate, pyqtSlot, QSize
# import cv2
# import glob
import sys
# import ctypes
import pymysql
import query_zip


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.__MEMOID = query_zip.get_id()

        self.__STATUS = 18  # 베트남대사관:0, 아포:1, 번역:2, 공증:3, 대사관:4, 계산서:5  첫번째 생성: 18, 두번째 셋팅:15
        self.__statusList = ["베트남대사관", "중국대사관", "번역", "공증", "국내아포스티유", "아포스티유", "아포스티유", "국내아포스티유",
                             "외국현지아포", "외교부아포", "번역공증",
                             "사실공증", "빠른베트남대사관1", "DHL베트남대사관1"]
        self.__datetime = QDateTime.currentDateTime()
        self.__completeDatetime = QDateTime.currentDateTime()

        buf_time = QTime()
        buf_time.setHMS(17, 0, 0)
        if self.__datetime.time() >= buf_time:
            self.__completeDatetime = self.__completeDatetime.addDays(1)

        self.__completeDatetime.setTime(buf_time)

        self.__save_table_items = []
        self.__tableHeader = ["유형", "내용", "작성날짜", "완결날짜", "완결", "삭제"]
        self.__tableHeader_compdel = ["유형", "내용", "작성날짜", "완결날짜", "복원"]

        self.__tablewidth = [113, 290, 173, 173, 55, 55]
        self.__tablewidth_compdel = [96, 297, 178, 178, 79]
        self.__savetablearray = []
        self.__listTable_count = 0
        self.__completeTable_count = 0
        self.__deleteTable_count = 0
        self.__statusList_select_switch = False
        self.__statusList_select_row = 29
        self.__timer_count = 0

        self.buf_timer_table = query_zip.get_table()

        self.initUI()

        self.__MEMOID = query_zip.get_id()

    def initUI(self):
        self.setWindowTitle('MemoApp')
        self.message = "{0}".format(self.__datetime.toString("MM월 dd일 dddd  ap hh:mm:ss"))
        self.statusBar().showMessage(self.message)
        self.resize(920, 879)
        self.center()
        self.centralWidget = QWidget(self)
        self.frameLayout = QVBoxLayout(self.centralWidget)

        ######## setLayout
        self.menuLayout = QHBoxLayout()
        self.menuLayout.setSpacing(7)
        self.displayLayout = QVBoxLayout()
        self.timeLayout = QHBoxLayout()
        self.contentsLayout = QVBoxLayout()
        self.comp_delLayout = QVBoxLayout()

        ######## setfunc
        self.statusMenu()
        self.statusDisplay()
        self.statusTime()
        self.statusContents()
        self.statusSummit()
        self.statusList()
        self.timer()
        self.completedList()
        self.deletedList()
        self.comp_delTab()

        self.get_table()

        ######## addLayout to frame
        self.frameLayout.addLayout(self.menuLayout)
        self.frameLayout.addLayout(self.displayLayout)
        self.frameLayout.addLayout(self.timeLayout)
        self.frameLayout.addLayout(self.contentsLayout)
        self.frameLayout.addWidget(self.summitBtn)
        self.frameLayout.addWidget(self.listTable)
        self.frameLayout.addLayout(self.comp_delLayout)

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

    def statusDisplay(self, reset=False):
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)

        stylesheet = self.edit_stylesheet()

        if reset == True:
            if self.__statusList_select_switch == True:
                self.listTable.showRow(self.__statusList_select_row)
                self.__statusList_select_row = 29
                self.__statusList_select_switch = False
                self.statusTextedit.setText("")
                self.__completeDatetime = QDateTime.currentDateTime()

                buf_time = QTime()
                buf_time.setHMS(17, 0, 0)
                self.__completeDatetime.setTime(buf_time)
                if self.__datetime.time() >= buf_time:
                    self.__completeDatetime = self.__completeDatetime.addDays(1)
                self.statusTime(reset=True)

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

    def statusContents(self, reset=False):
        buf_text = ""
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        font.setBold(False)

        stylesheet = self.edit_stylesheet()

        if reset == True:
            self.__STATUS == 15

        if 0 <= self.__STATUS <= len(self.statusLabels):
            if self.statusTextedit.toPlainText() != "": buf_text = self.statusTextedit.toPlainText()
            self.statusTextedit.deleteLater()
            self.statusTextedit = None
            self.statusTextedit = QTextEdit()
            self.statusTextedit.setFixedHeight(161)
            self.statusTextedit.setText(buf_text)
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(stylesheet[self.__statusList[self.__STATUS]])
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.contentsLayout.addWidget(self.statusTextedit)


        elif self.__STATUS == 15:
            if self.statusTextedit.toPlainText() != "": buf_text = self.statusTextedit.toPlainText()
            self.statusTextedit.deleteLater()
            self.statusTextedit = None
            self.statusTextedit = QTextEdit()
            self.statusTextedit.setFixedHeight(161)
            self.statusTextedit.setText(buf_text)
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(stylesheet['보통'])
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.contentsLayout.addWidget(self.statusTextedit)

        elif self.__STATUS == 18:
            self.__STATUS == 15
            self.statusTextedit = QTextEdit()
            self.statusTextedit.setFixedHeight(161)
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(stylesheet['보통'])
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.contentsLayout.addWidget(self.statusTextedit)

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
        self.__completeDatetime.date

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
        if self.__datetime < self.__completeDatetime:
            self.__completeDatetime = self.__completeDatetime.addDays(-1)
            completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
            self.completeDateLabel.setText(completeDate)
            self.timeLayout.update()

    def downTimeBtn_clicked(self):
        self.__completeDatetime = self.__completeDatetime.addSecs(1800)
        completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
        completeTime = self.__completeDatetime.toString("ap hh:mm")
        self.completeDateLabel.setText(completeDate)
        self.completeTimeLabel.setText(completeTime)
        self.timeLayout.update()

    def upTimeBtn_clicked(self):
        self.__completeDatetime = self.__completeDatetime.addSecs(-1800)
        completeDate = self.__completeDatetime.toString("MM월 dd일 dddd")
        completeTime = self.__completeDatetime.toString("ap hh:mm")
        self.completeDateLabel.setText(completeDate)
        self.completeTimeLabel.setText(completeTime)
        self.timeLayout.update()

    def statusList(self):
        self.listTable = QTableWidget(self.centralWidget)
        self.listTable.setLineWidth(1)
        self.listTable.setColumnCount(6)
        self.listTable.setHorizontalHeaderLabels(self.__tableHeader)
        self.listTable.itemClicked.connect(self.statusList_selected)
        _ = [self.listTable.setColumnWidth(idx, width)
             for idx, width in enumerate(self.__tablewidth)]

    def get_table(self):
        rowCount = self.listTable.rowCount()
        normalTable, completeTable = query_zip.get_table()
        completeTable = completeTable[::-1]
        completeTable = completeTable[:5]

        self.listTable.setRowCount(len(normalTable))
        self.__listTable_count = len(normalTable)

        brushColor = self.edit_stylesheet(type="brushColor")

        styleSheet = self.edit_stylesheet(color=True,
                                          background_color=True,
                                          border_color=False,
                                          border_radius=False,
                                          border_width=False,
                                          border_style=False)

        for idx, i in enumerate(normalTable):
            brush = QBrush(brushColor[self.__statusList[i[1]]])
            brush.setStyle(Qt.SolidPattern)
            rowItem = [self.__statusList[i[1]], i[2], i[3], i[4], "완결", "삭제"]

            for idx_contents, item in enumerate(rowItem):
                if idx_contents == 0:
                    font = QFont()
                    font.setFamily("맑은 고딕")
                    font.setPointSize(11)
                    font.setBold(True)
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(str(item))
                    setitem.setTextAlignment(Qt.AlignCenter)
                    setitem.setFlags(Qt.ItemIsEditable)
                    setitem.setFont(font)
                    buf_item = self.listTable.setItem(idx, 0, setitem)

                elif idx_contents == 1 or idx_contents == 2 or idx_contents == 3:
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(str(item))
                    setitem.setTextAlignment(Qt.AlignCenter)
                    buf_item = self.listTable.setItem(idx, idx_contents, setitem)

                elif idx_contents == 4:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(str(item))
                    buf_item.clicked.connect(self.completeClicked)
                    buf_item.setFixedWidth(self.__tablewidth[idx_contents])
                    buf_item.setStyleSheet(styleSheet[rowItem[0]])
                    self.listTable.setCellWidget(idx, 4, buf_item)

                elif idx_contents == 5:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(str(item))
                    buf_item.clicked.connect(self.deleteClicked)
                    buf_item.setFixedWidth(self.__tablewidth[idx_contents])
                    buf_item.setStyleSheet(styleSheet[rowItem[0]])
                    self.listTable.setCellWidget(idx, 5, buf_item)

        self.completeList.setRowCount(len(completeTable))
        self.__completeTable_count = len(completeTable)

        complete_brush = self.edit_stylesheet(type="complete_brush")
        complete_styleSheet = self.edit_stylesheet(color=True,
                                                   background_color=True,
                                                   border_color=False,
                                                   border_radius=False,
                                                   border_width=False,
                                                   border_style=False)
        for idx,j in enumerate(completeTable):
            buf_text = [j[i] for i in range(5)]

            buf_text = buf_text[1:]
            buf_text[0] = self.__statusList[buf_text[0]]

            for i in range(4):

                if i == 0:
                    buf_state = self.__statusList[j[1]]

                buf_item = QTableWidgetItem()
                buf_item.setTextAlignment(Qt.AlignCenter)
                buf_item.setBackground(complete_brush[buf_state])
                buf_item.setFlags(Qt.ItemIsEditable)
                buf_item.setText(buf_text[i])

                if i == 0:
                    self.completeList.setItem(idx, 0, buf_item)
                else:
                    self.completeList.setItem(idx, i, buf_item)

            buf_btn = QPushButton()
            buf_btn.clicked.connect(self.comp_recoverCliked)
            buf_btn.setText(self.__tableHeader_compdel[4])
            buf_btn.setStyleSheet(complete_styleSheet[buf_state])
            self.completeList.setCellWidget(idx, 4, buf_btn)

        self.update()

    def statusList_selected(self):

        if self.__statusList_select_switch is not True:
            row = self.listTable.currentRow()

            self.__statusList_select_switch = True
            self.__statusList_select_row = row

            status = self.listTable.item(row, 0).text()
            self.__STATUS = self.__statusList.index(status)
            contents = self.listTable.item(row, 1).text()

            self.statusContents()
            self.statusTextedit.setText(contents)

            target_date = self.listTable.item(row, 3).text()
            buf_date = QDate.fromString(target_date[:7], "MM월 dd일")
            buf_date.setDate(self.__datetime.date().year(), buf_date.month(), buf_date.day())
            buf_time = QTime.fromString(target_date[-8:], "ap hh:mm")

            self.__completeDatetime.setDate(buf_date)
            self.__completeDatetime.setTime(buf_time)

            self.listTable.hideRow(row)

            self.statusDisplay()
            self.statusTime(reset=True)

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

        if self.__statusList_select_switch == True:
            self.listTable.removeRow(self.__statusList_select_row)
            self.__listTable_count -= 1
            self.__statusList_select_row = 29

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

            rowItem = [self.__statusList[self.__STATUS],
                       statusContents,
                       self.__datetime.toString("MM월 dd일 dddd  ap hh:mm"),
                       self.__completeDatetime.toString("MM월 dd일 dddd  ap hh:mm"),
                       "완결",
                       "삭제"]

            self.__listTable_count += 1
            self.listTable.setRowCount(self.__listTable_count)

            for idx, item in enumerate(rowItem):

                if idx == 0:
                    font = QFont()
                    font.setFamily("맑은 고딕")
                    font.setPointSize(11)
                    font.setBold(True)
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(str(item))
                    setitem.setTextAlignment(Qt.AlignCenter)
                    setitem.setFlags(Qt.ItemIsEditable)
                    setitem.setFont(font)
                    buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

                elif idx == 1 or idx == 2:
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(str(item))
                    setitem.setTextAlignment(Qt.AlignCenter)
                    buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

                elif idx == 3:
                    setitem = QTableWidgetItem()
                    setitem.setBackground(brush)
                    setitem.setText(str(item))
                    setitem.setTextAlignment(Qt.AlignCenter)
                    buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

                elif idx == 4:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(str(item))
                    buf_item.clicked.connect(self.completeClicked)
                    buf_item.setFixedWidth(self.__tablewidth[idx])
                    buf_item.setStyleSheet(styleSheet[self.__statusList[self.__STATUS]])
                    self.listTable.setCellWidget(self.__listTable_count - 1, idx, buf_item)

                elif idx == 5:
                    buf_item = QPushButton(self.centralWidget)
                    buf_item.setText(str(item))
                    buf_item.clicked.connect(self.deleteClicked)
                    buf_item.setFixedWidth(self.__tablewidth[idx])
                    buf_item.setStyleSheet(styleSheet[self.__statusList[self.__STATUS]])
                    self.listTable.setCellWidget(self.__listTable_count - 1, idx, buf_item)

            if self.__statusList_select_switch == False:
                query_zip.increase_id()
                self.__MEMOID = query_zip.get_id()
                query_zip.insert([self.__MEMOID, self.__STATUS, statusContents, rowItem[2], rowItem[3], 0, 0,
                                  self.__datetime.toString("MM월 dd일 dddd  ap hh:mm")])
            else:
                # query_zip.update(1,1)
                self.__statusList_select_switch = False

            self.statusTextedit.setText("")
            self.resetTool(save_event=True)
            self.update()

    def completedList(self):
        self.completeList = QTableWidget()
        self.completeList.setLineWidth(1)
        self.completeList.setColumnCount(5)
        self.completeList.setHorizontalHeaderLabels(self.__tableHeader_compdel)
        _ = [self.completeList.setColumnWidth(idx, width)
             for idx, width in enumerate(self.__tablewidth_compdel)]

    def deletedList(self):
        self.deleteList = QTableWidget()
        self.deleteList.setLineWidth(1)
        self.deleteList.setColumnCount(5)
        self.deleteList.setHorizontalHeaderLabels(self.__tableHeader_compdel)
        _ = [self.deleteList.setColumnWidth(idx, width)
             for idx, width in enumerate(self.__tablewidth_compdel)]

    def comp_delTab(self):
        self.comp_delTab = QTabWidget()
        self.comp_delTab.setFixedHeight(116)
        self.comp_delTab.addTab(self.completeList, "완결")
        self.comp_delTab.addTab(self.deleteList, "삭제")
        self.comp_delLayout.addWidget(self.comp_delTab)

    @pyqtSlot()
    def completeClicked(self):
        button = self.sender()
        complete_brush = self.edit_stylesheet(type="complete_brush")
        complete_styleSheet = self.edit_stylesheet(color=True,
                                                   background_color=True,
                                                   border_color=False,
                                                   border_radius=False,
                                                   border_width=False,
                                                   border_style=False)
        if button:
            row = self.listTable.indexAt(button.pos()).row()
            buf_text = [self.listTable.item(row, i).text() for i in range(4)]

            self.__completeTable_count += 1
            self.completeList.setRowCount(self.__completeTable_count)

            for i in range(4):
                if i == 0: buf_state = self.listTable.item(row, i).text()
                buf_item = QTableWidgetItem()
                buf_item.setTextAlignment(Qt.AlignCenter)
                buf_item.setBackground(complete_brush[buf_state])
                buf_item.setFlags(Qt.ItemIsEditable)
                if i == 3:
                    buf_item.setText(self.__datetime.toString("MM월 dd일 dddd  ap hh:mm"))
                else:
                    buf_item.setText(buf_text[i])

                self.completeList.setItem(self.__completeTable_count - 1, i, buf_item)

            buf_btn = QPushButton()
            buf_btn.clicked.connect(self.comp_recoverCliked)
            buf_btn.setText(self.__tableHeader_compdel[4])
            buf_btn.setStyleSheet(complete_styleSheet[buf_state])
            self.completeList.setCellWidget(self.__completeTable_count - 1, 4, buf_btn)

            itemlist = buf_text
            itemlist[0] = self.__statusList.index(itemlist[0])

            query_zip.update(itemlist, ["", "", "", "", "1", "", ""])

            self.listTable.removeRow(row)
            self.__listTable_count -= 1

    @pyqtSlot()
    def comp_recoverCliked(self):
        button = self.sender()
        if button:
            row = self.completeList.indexAt(button.pos()).row()
            buf_text = [self.completeList.item(row, i).text() for i in range(4)]

        brushColor = self.edit_stylesheet(type="brushColor")
        brush = QBrush(brushColor[buf_text[0]])
        brush.setStyle(Qt.SolidPattern)
        styleSheet = self.edit_stylesheet(color=True,
                                          background_color=True,
                                          border_color=False,
                                          border_radius=False,
                                          border_width=False,
                                          border_style=False)

        self.__listTable_count += 1
        self.listTable.setRowCount(self.__listTable_count)

        rowItem = [buf_text[0], buf_text[1], buf_text[2], buf_text[3], "완결", "삭제"]

        for idx, item in enumerate(rowItem):
            if idx == 0:
                font = QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(11)
                font.setBold(True)
                setitem = QTableWidgetItem()
                setitem.setBackground(brush)
                setitem.setText(str(item))
                setitem.setTextAlignment(Qt.AlignCenter)
                setitem.setFlags(Qt.ItemIsEditable)
                setitem.setFont(font)
                buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

            elif idx == 1 or idx == 2:
                setitem = QTableWidgetItem()
                setitem.setBackground(brush)
                setitem.setText(str(item))
                setitem.setTextAlignment(Qt.AlignCenter)
                buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

            elif idx == 3:
                setitem = QTableWidgetItem()
                setitem.setBackground(brush)
                setitem.setText(self.__completeDatetime.toString("MM월 dd일 dddd  ap hh:mm"))
                setitem.setTextAlignment(Qt.AlignCenter)
                buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

            elif idx == 4:
                buf_item = QPushButton()
                buf_item.setText(str(item))
                buf_item.clicked.connect(self.completeClicked)
                buf_item.setFixedWidth(self.__tablewidth[idx])
                buf_item.setStyleSheet(styleSheet[buf_text[0]])
                self.listTable.setCellWidget(self.__listTable_count - 1, idx, buf_item)

            elif idx == 5:
                buf_item = QPushButton()
                buf_item.setText(str(item))
                buf_item.clicked.connect(self.deleteClicked)
                buf_item.setFixedWidth(self.__tablewidth[idx])
                buf_item.setStyleSheet(styleSheet[buf_text[0]])
                self.listTable.setCellWidget(self.__listTable_count - 1, idx, buf_item)

        itemlist = rowItem
        itemlist[0] = self.__statusList.index(itemlist[0])

        query_zip.update(itemlist, ["", "", "", "", "0", "", ""])

        self.completeList.removeRow(row)
        self.__completeTable_count -= 1

    @pyqtSlot()
    def deleteClicked(self):
        button = self.sender()
        complete_brush = self.edit_stylesheet(type="complete_brush")
        complete_styleSheet = self.edit_stylesheet(color=True,
                                                   background_color=True,
                                                   border_color=False,
                                                   border_radius=False,
                                                   border_width=False,
                                                   border_style=False)
        if button:
            row = self.listTable.indexAt(button.pos()).row()
            buf_text = [self.listTable.item(row, i).text() for i in range(4)]

            self.__deleteTable_count += 1
            self.deleteList.setRowCount(self.__deleteTable_count)

            for i in range(4):
                if i == 0: buf_state = self.listTable.item(row, i).text()
                buf_item = QTableWidgetItem()
                buf_item.setText(buf_text[i])
                buf_item.setTextAlignment(Qt.AlignCenter)
                buf_item.setBackground(complete_brush[buf_state])
                self.deleteList.setItem(self.__deleteTable_count - 1, i, buf_item)

            buf_btn = QPushButton()
            buf_btn.clicked.connect(self.del_recoverCliked)
            buf_btn.setText(self.__tableHeader_compdel[4])
            buf_btn.setStyleSheet(complete_styleSheet[buf_state])
            self.deleteList.setCellWidget(self.__deleteTable_count - 1, 4, buf_btn)

            itemlist = buf_text
            itemlist[0] = self.__statusList.index(itemlist[0])

            query_zip.update(itemlist, ["", "", "", "", "", "1", ""])


            self.listTable.removeRow(row)
            self.__listTable_count -= 1

    @pyqtSlot()
    def del_recoverCliked(self):
        button = self.sender()
        if button:
            row = self.deleteList.indexAt(button.pos()).row()
            buf_text = [self.deleteList.item(row, i).text() for i in range(4)]

        brushColor = self.edit_stylesheet(type="brushColor")
        brush = QBrush(brushColor[buf_text[0]])
        brush.setStyle(Qt.SolidPattern)
        styleSheet = self.edit_stylesheet(color=True,
                                          background_color=True,
                                          border_color=False,
                                          border_radius=False,
                                          border_width=False,
                                          border_style=False)

        self.__listTable_count += 1
        self.listTable.setRowCount(self.__listTable_count)

        rowItem = [buf_text[0], buf_text[1], buf_text[2], buf_text[3], "완결", "삭제"]

        for idx, item in enumerate(rowItem):

            if idx == 0:
                font = QFont()
                font.setFamily("맑은 고딕")
                font.setPointSize(11)
                font.setBold(True)
                setitem = QTableWidgetItem()
                setitem.setBackground(brush)
                setitem.setText(str(item))
                setitem.setTextAlignment(Qt.AlignCenter)
                setitem.setFlags(Qt.ItemIsEditable)
                setitem.setFont(font)
                buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

            elif idx == 1 or idx == 2:
                setitem = QTableWidgetItem()
                setitem.setBackground(brush)
                setitem.setText(str(item))
                setitem.setTextAlignment(Qt.AlignCenter)
                buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

            elif idx == 3:
                setitem = QTableWidgetItem()
                setitem.setBackground(brush)
                setitem.setText(str(item))
                setitem.setTextAlignment(Qt.AlignCenter)
                buf_item = self.listTable.setItem(self.__listTable_count - 1, idx, setitem)

            elif idx == 4:
                buf_item = QPushButton()
                buf_item.setText(str(item))
                buf_item.clicked.connect(self.completeClicked)
                buf_item.setFixedWidth(self.__tablewidth[idx])
                buf_item.setStyleSheet(styleSheet[buf_text[0]])
                self.listTable.setCellWidget(self.__listTable_count - 1, idx, buf_item)

            elif idx == 5:
                buf_item = QPushButton()
                buf_item.setText(str(item))
                buf_item.clicked.connect(self.deleteClicked)
                buf_item.setFixedWidth(self.__tablewidth[idx])
                buf_item.setStyleSheet(styleSheet[buf_text[0]])
                self.listTable.setCellWidget(self.__listTable_count - 1, idx, buf_item)

        self.deleteList.removeRow(row)
        self.__deleteTable_count -= 1

    def timer(self):
        self.Qtimer = QTimer()
        self.Qtimer.timeout.connect(self.updatetime_alram)
        self.timerswitch = False
        self.Qtimer.start(1000)

    def updatetime_alram(self):
        complete_brush = self.edit_stylesheet(type="complete_brush")
        self.__datetime = QDateTime.currentDateTime()
        self.statusBar().showMessage(self.__datetime.toString("MM월 dd일 dddd  ap hh:mm:ss"))

        buf_timer = 0
        buf_timer1 = 0

        for i in range(self.listTable.rowCount()):
            buf_date = QDate.fromString(self.listTable.item(i, 3).text()[:7], "MM월 dd일")
            buf_date.setDate(self.__datetime.date().year(), buf_date.month(), buf_date.day())
            buf_time = QTime.fromString(self.listTable.item(i, 3).text()[-8:], "ap hh:mm")
            buf_state = self.listTable.item(i, 0).text()
            comp_time = QTime()

            comp_hours = self.__datetime.time().hour()
            comp_minute = self.__datetime.time().minute()

            comp_time.setHMS(comp_hours, comp_minute, 0)

            buf_date.setDate(self.__datetime.date().year(), buf_date.month(), buf_date.day())

            for j in range(4):
                if buf_date == self.__datetime.date():
                    if buf_time <= self.__datetime.time():
                        self.listTable.item(i, j).setBackground(complete_brush[buf_state])

            if buf_date <= self.__datetime.date():

                if buf_time <= comp_time.addSecs(15 * 60):
                    if buf_timer == 0 or buf_time == 15 * 60 + 1:
                        if self.timerswitch == False:
                            font = QFont()
                            font.setFamily("맑은 고딕")
                            font.setPointSize(15)
                            font.setBold(True)
                            msg = QMessageBox()
                            msg.resize(1000, 200)
                            msg.setWindowTitle("                           완결 15분전 알리미                           ")
                            buf_text = "\n\n완결 15분전 : {}\n\n{}\n\n ".format(self.listTable.item(i, 0).text(),
                                                                            self.listTable.item(i, 1).text())
                            msg.setText(buf_text)
                            msg.setFont(font)
                            ret = msg.exec_()
                        buf_timer = 0
                        self.timerswitch = True

                    buf_timer += 1

                elif buf_time <= comp_time:

                    if buf_timer1 == 0 or buf_timer1 <= 15:
                        if self.timerswitch == False:
                            font = QFont()
                            font.setFamily("맑은 고딕")
                            font.setPointSize(15)
                            font.setBold(True)
                            msg = QMessageBox()
                            msg.resize(1000, 200)
                            msg.setWindowTitle("                           완결 알리미                           ")
                            buf_text = "\n\n{}\n\n{}\n\n ".format(self.listTable.item(i, 0).text(),
                                                                  self.listTable.item(i, 1).text())
                            msg.setText(buf_text)
                            msg.setFont(font)
                            ret = msg.exec_()
                            itemlist = [self.listTable.item(i, k).text() for k in range(4)]
                            itemlist[0] = self.__statusList.index(itemlist[0])

                            query_zip.update(itemlist, ["", "", "", "", "1", "", ""])

                            buf_timer1 = 0
                            self.timerswitch = True

                        buf_timer1 += 1

        self.__timer_count += 1

        if self.__timer_count == 5:
            self.__timer_count = 0
            if self.buf_timer_table != query_zip.get_table():
                self.buf_timer_table == query_zip.get_table()
                self.get_table()

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
                    # if self.__STATUS == 15:
                    #     if self.statusTextedit.toPlainText() != "" :
                    #         buf_text = self.statusTextedit.toPlainText()
                    self.__STATUS = idx

        if self.__STATUS == 18: self.__STATUS = 15  # fix menu error

        self.resetTool(mouse_event=True)
        self.update()

    def resetTool(self,
                  mouse_event=False,
                  save_event=False,
                  time_event=False):

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

            if self.__datetime.time() >= buf_time:
                self.__completeDatetime = self.__completeDatetime.addDays(1)

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
                        border_style=True,
                        border_width=True,
                        border_color=True,
                        border_radius=True,
                        type="styleSheet"):

        if type == "styleSheet":
            menuList = ["베트남대사관", "중국대사관", "번역", "공증", "국내아포스티유", "아포스티유", "보통"]
            buf_string = ""
            buf_dic = {}
            stylesheet = {"베트남대사관": ["black;",  # 빨간색
                                  "#abd1ff;",
                                  "solid;",
                                  "3px;",
                                  "#7EB9FF;",
                                  "8px"],
                          "중국대사관": ["black;",  # 주황색
                                    "#fe8e8e;",
                                    "solid;",
                                    "3px;",
                                    "#fe4141;",
                                    "8px"],
                          "번역": ["black;",  # 초록색
                                 "#cfeb8a;",
                                 "solid;",
                                 "3px;",
                                 "#b3eb2b;",
                                 "8px"],
                          "공증": ["black;",  # 초록색
                                 "#ffa370;",
                                 "solid;",
                                 "3px;",
                                 "#fe833e;",
                                 "8px"],
                          "국내아포스티유": ["black;",  # 보라색
                                 "#e3c4ff;",
                                 "solid;",
                                 "3px;",
                                 "#C486FF;",
                                 "8px"],

                          "아포스티유": ["black;",  # 노란색
                                     "#ffffb8;",
                                     "solid;",
                                     "3px;",
                                     "#e3e472;",
                                     "8px"],
                          "보통": ["gray;",
                                 "#dadada;",
                                 "solid;",
                                 "2px;",
                                 "#dadada;",
                                 "3px"]
                          }
            for list in menuList:
                if color == True:
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

            return buf_dic

        elif type == "brushColor":
            brushColor = {"베트남대사관": QColor(171, 209, 254),
                          "중국대사관": QColor(254, 80, 80),
                          "번역": QColor(207, 235, 138),
                          "공증": QColor(254, 131, 62),
                          "국내아포스티유": QColor(227, 196, 254),
                          "아포스티유": QColor(254, 254, 184),
                          }
            return brushColor

        elif type == "complete_brush":
            brushColor = {"베트남대사관": QColor(171, 209, 254),
                          "중국대사관": QColor(254, 80, 80),
                          "번역": QColor(207, 235, 138),
                          "공증": QColor(254, 131, 62),
                          "국내아포스티유": QColor(227, 196, 254),
                          "아포스티유": QColor(254, 254, 184),
                          }
            brush = {}
            for color in brushColor:
                buf_Qbrush = QBrush()
                buf_Qbrush.setStyle(Qt.DiagCrossPattern)
                buf_Qbrush.setColor(brushColor[color])
                brush[color] = buf_Qbrush

            return brush


if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())