import sys


from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import QDate, Qt


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.pos1 = [0, 0]
        self.label()
        self.initUI()
        self.setMouseTracking(True)


    def initUI(self):
        self.setWindowTitle('My First Application')
        now = QDate.currentDate()
        message = "{0}     {1}".format("Ready",now.toString(Qt.DefaultLocaleLongDate))
        self.label()
        self.statusBar().showMessage(message)
        self.setWindowTitle('Statusbar')
        self.move(300, 300)
        self.resize(400, 500)
        self.center()
        self.show()

    # def mouseMoveEvent(self, event):
    #     self.setMouseTracking(True)
    #     now = QDate.currentDate()
    #     message = "{0}     {1}     Mouse 위치 ; x={2},y={3}, global={4},{5}".\
    #         format("Ready",now.toString(Qt.DefaultLocaleLongDate), event.x(), event.y(), event.globalX(), event.globalY())
    #     self.statusBar().showMessage(message)

    def mousePressEvent(self, event):
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        self.mousePR = True
        self.update()

    def mouseReleaseEvent(self, event):
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        self.mousePR = False
        self.update()

    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())

    def label(self):
        self.centralWidget = QWidget(self)
        lbl_red = QLabel(self.centralWidget)
        lbl_green = QLabel(self.centralWidget)
        lbl_blue = QLabel(self.centralWidget)
        lbl_red.setStyleSheet("color: red;"
                                  "border-style: solid;"
                                  "border-width: 2px;"
                                  "border-color: #FA8072;"
                                  "border-radius: 3px")

        lbl_green.setStyleSheet("color: green;"
                                    "background-color: #7FFFD4")

        lbl_blue.setStyleSheet("color: blue;"
                                   "background-color: #87CEFA;"
                                   "border-style: dashed;"
                                   "border-width: 3px;"
                                   "border-color: #1E90FF")

        vbox = QVBoxLayout(self.centralWidget)

        vbox.addWidget(lbl_red)
        vbox.addWidget(lbl_green)
        vbox.addWidget(lbl_blue)

        self.setCentralWidget(self.centralWidget)

    def paintEvent(self, event):
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





if __name__ == '__main__':

    app = QApplication(sys.argv)
    windowapp = MainWindow()


    sys.exit(app.exec_())