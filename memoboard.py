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
        date = QDate.currentDate()
        date = date.toString(Qt.DefaultLocaleLongDate)
        print(date)
        time = QTime.currentTime()
        self.datetime = "{0}  {1}".format(date, time.toString())
        self.initUI()
        self.setMouseTracking(True)

    def initUI(self):
        self.setWindowTitle('Memoboard')
        message = "{0}     {1}".format("Ready", self.datetime)
        self.STATUS = 18
        self.statusBar().showMessage(message)
        self.resize(774, 879)
        self.center()

        self.centralWidget = QWidget(self)
        self.framebox = QVBoxLayout(self.centralWidget)

        self.status_menu()
        self.status_label_layout = QVBoxLayout()
        self.status_label()
        self.status_textedit_layout = QVBoxLayout()
        self.status_textedit()
        self.status_btn()
        self.save_table()

        self.framebox.addLayout(self.status_menulayout)
        self.framebox.addLayout(self.status_label_layout)
        self.framebox.addLayout(self.status_textedit_layout)
        self.framebox.addLayout(self.save_btn_layout)
        self.framebox.addLayout(self.save_table_layout)
        spacerItem = QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.framebox.addItem(spacerItem)

        self.setCentralWidget(self.centralWidget)
        self.show()

    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())

    def status_menu(self):

        self.status = ["대사관", "아포스티유", "공증", "등기", "견적서", "계산서"]
        self.status_stylesheet = {"대사관": "color: black;"  # 빨간색
                                         "background-color: #7EB9FF;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #7EB9FF;"
                                         "border-radius: 8px",
                                  "아포스티유": "color: black;"  # 주황색
                                           "background-color: #ff917b;"
                                           "border-style: solid;"
                                           "border-width: 3px;"
                                           "border-color: #ff917b;"
                                           "border-radius: 8px",
                                  "공증": "color: black;"  # 초록색
                                        "background-color: #b3eb2b;"
                                        "border-style: solid;"
                                        "border-width: 3px;"
                                        "border-color: #b3eb2b;"
                                        "border-radius: 8px",
                                  "등기": "color: black;"  # 보라색
                                        "background-color: #C486FF;"
                                        "border-style: solid;"
                                        "border-width: 3px;"
                                        "border-color: #C486FF;"
                                        "border-radius: 8px",
                                  "견적서": "color: black;"  # 노란색
                                         "background-color: #FEFF7F;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #FEFF7F;"
                                         "border-radius: 8px",
                                  "계산서": "color: black;"  # 노란색
                                         "background-color: #FEFF7F;"
                                         "border-style: solid;"
                                         "border-width: 3px;"
                                         "border-color: #FEFF7F;"
                                         "border-radius: 8px"
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
            print(item.x())

        # print(self.status_stylesheet["계산서"])

        # self.textEdit = QTextEdit(self.centralWidget)
        # self.textEdit.setMaximumSize(QSize(16777215, 200))
        # self.vbox.addWidget(self.textEdit)

        # labeltest = QLabel(self.centralWidget)
        # labeltest.setText("111")
        # self.vbox.addWidget(labeltest)

        self.hbox = QHBoxLayout()
        self.hbox.setSpacing(7)

        for idx, label in enumerate(self.labels):
            # item.resize(wide,50)
            # item.move(wide*(idx)+10,10)
            label.setFixedHeight(50)
            self.hbox.addWidget(label)
            print(label.width())

        self.status_menulayout = QVBoxLayout()
        self.status_menulayout.addLayout(self.hbox)

    def status_label(self):

        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(18)
        font.setBold(True)
        self.normal_stylesheet = {"normal": "color: gray;"  # 빨간색
                                            "border-style: solid;"
                                            "border-width: 2px;"
                                            "border-color: gray;"
                                            "border-radius: 3px"}

        if 0 <= self.STATUS <= len(self.labels):
            self.statusLabel.deleteLater()
            self.statusLabel = None
            self.statusLabel = QLabel(self.centralWidget)
            self.statusLabel.setFont(font)
            self.statusLabel.setStyleSheet(self.status_stylesheet[self.status[self.STATUS]])
            self.statusLabel.setText("유 형 : {}".format(self.status[self.STATUS]))
            self.statusLabel.setAlignment(Qt.AlignLeft)
            self.status_label_layout.addWidget(self.statusLabel)

        else:
            if self.STATUS == 15:
                self.statusLabel.deleteLater()
                self.statusLabel = None
                self.statusLabel = QLabel(self.centralWidget)
                self.statusLabel.setFont(font)
                self.statusLabel.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusLabel.setText("유 형 : 선택해주세요.")
                self.statusLabel.setAlignment(Qt.AlignLeft)
                self.status_label_layout.addWidget(self.statusLabel)

            elif self.STATUS == 18:
                self.statusLabel = QLabel(self.centralWidget)
                self.statusLabel.setFont(font)
                self.statusLabel.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusLabel.setText("유 형 : 선택해주세요.")
                self.statusLabel.setAlignment(Qt.AlignLeft)
                self.status_label_layout.addWidget(self.statusLabel)

        self.status_label_layout.update()

    def status_textedit(self):
        font = QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        font.setBold(False)

        if 0 <= self.STATUS <= len(self.labels):
            self.statusTextedit.deleteLater()
            self.statusTextedit = None
            self.statusTextedit = QTextEdit(self.centralWidget)
            self.statusTextedit.setFont(font)
            self.statusTextedit.setStyleSheet(self.status_stylesheet[self.status[self.STATUS]])
            self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
            self.statusTextedit.setAlignment(Qt.AlignLeft)
            self.status_textedit_layout.addWidget(self.statusTextedit)
        else:
            if self.STATUS == 15:
                self.statusTextedit.deleteLater()
                self.statusTextedit = None
                self.statusTextedit = QTextEdit(self.centralWidget)
                self.statusTextedit.setFont(font)
                self.statusTextedit.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
                self.statusTextedit.setAlignment(Qt.AlignLeft)
                self.status_textedit_layout.addWidget(self.statusTextedit)

            elif self.STATUS == 18:
                self.statusTextedit = QTextEdit(self.centralWidget)
                self.statusTextedit.setPlaceholderText('메모내용을 입력하세요.')
                self.statusTextedit.setFont(font)
                self.statusTextedit.setStyleSheet(self.normal_stylesheet['normal'])
                self.statusTextedit.setAlignment(Qt.AlignLeft)
                self.status_textedit_layout.addWidget(self.statusTextedit)

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
        self.tableHeader = ["유형", "내용", "작성날짜", "완결", "삭제"]
        tablewidth = [80, 320, 200, 70, 70]
        self.saveTable = QTableWidget(self.centralWidget)
        self.saveTable.setLineWidth(1)
        self.saveTable.setObjectName("tableWidget")
        self.saveTable.setColumnCount(5)
        self.saveTable.setHorizontalHeaderLabels(self.tableHeader)
        settablewidth = [self.saveTable.setColumnWidth(idx, width)
                         for idx, width in enumerate(tablewidth)]

        # self.saveTable.setRowCount(self.SAVE_TABLE_COUNT)
        #
        #
        # buf_item = QLabel(self.centralWidget)
        # buf_item.setText('1111111111')
        #
        # buf_item.setStyleSheet(self.status_stylesheet[self.status[3]])
        #
        # self.saveTable.setItem(self.SAVE_TABLE_COUNT - 1, 0, QTableWidgetItem(buf_item))

        self.save_table_layout.addWidget(self.saveTable)
        self.save_table_layout.update()

    def keyPressEvent(self, event):
        if event.key() in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Space]:  ## Trigger Edit
            print('@@@@@@@@@@@@@@@@')

    def mousePressEvent(self, event):
        self.pos1 = [0, 0]
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        buf_STATUS = self.STATUS
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
        # message = "{0}     {1}     Mouse 위치 ; x={2},y={3}, global={4},{5}". \
        #             format("누름",self.time.toString(Qt.DefaultLocaleLongDate), event.x(), event.y(), event.globalX(), event.globalY())
        posmee = "{}".format(label_size)  # self.labels[0].width())
        print(label_section)

        for idx, section in enumerate(label_section):
            if section[0] <= self.pos1[0] <= section[1]:
                if section[2] <= self.pos1[1] <= section[3]:
                    print(self.status[idx])
                    self.STATUS = idx

        if buf_STATUS == self.STATUS:
            self.STATUS = 15

        self.status_label()
        self.status_textedit()
        self.statusBar().showMessage(posmee)

        self.update()

    def save_btn_clicked(self):
        statusTextedit = self.statusTextedit.toPlainText()
        if not (0 <= self.STATUS <= len(self.status)) \
                or (len(statusTextedit) == 0):
            self.save_btn.setText("유형을 선택해주세요.")
            if not (0 <= self.STATUS <= len(self.status)):
                self.save_btn.setText("유형을 선택해주세요.")
            elif len(statusTextedit) == 0:
                self.save_btn.setText("내용을 입력해주세요.")
        else:
            self.save_btn.setText("입력")

            self.save_table_additems = [self.status[self.STATUS],
                                        statusTextedit,
                                        self.datetime,
                                        "btn",
                                        "btn"]

            self.SAVE_TABLE_COUNT += 1

            # print(self.SAVE_TABLE_COUNT, self.save_table_additems)

            self.saveTable.setRowCount(self.SAVE_TABLE_COUNT)

            for idx, item in enumerate(self.save_table_additems):
                buf_item = QLabel(self.centralWidget)
                buf_item.setText(item)
                # print(item, self.status_stylesheet[self.status[self.STATUS]][:-19])
                buf_item.setStyleSheet(self.status_stylesheet[self.status[self.STATUS]][:-19])
                buf_item.setAlignment(Qt.AlignCenter)
                self.saveTable.setCellWidget(self.SAVE_TABLE_COUNT - 1, idx, buf_item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    memoapp = MainWindow()

    sys.exit(app.exec_())