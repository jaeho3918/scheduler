import sys


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import numpy as np
import cv2
import glob

class OverLay(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(80, 80, 255, 128))

class Filter(QObject):
    def __init__(self, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.m_overlay = None
        self.m_overlayOn = None

    def eventFilter(self, obj, event):
        if not obj.isWidgetType():
            return False
        if event.type() == QEvent.MouseButtonPress:
            if not self.m_overlay:
                self.m_overlay = OverLay(obj.parentWidget())
            self.m_overlay.setGeometry(obj.geometry())
            self.m_overlayOn = obj
            self.m_overlay.show()
        elif event.type() == QEvent.Resize:
            if self.m_overlay and self.m_overlayOn == obj:
                self.m_overlay.setGeometry(obj.geometry())
        return False

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.pos1 = [0, 0]
        self.now = QDate.currentDate()
        self.label()
        self.initUI()
        self.setMouseTracking(True)
        self.filt = Filter()

    def imageset(self):
        self.images=[]
        for path_images in glob.glob(".\\*.png"):
            self.images.append(cv2.imread(path_images))

        self.pixmap_label = QLabel(self.centralWidget)
        self.pixmap_label.setStyleSheet("color: black;"
                              "border-style: solid;"
                              "border-width: 2px;"
                              "border-color: #FA8072;"
                              "border-radius: 3px")
        self.pixmap_label.setText('뀨뀨뀨뀨뀨뀨뀨')
        self.pixmap_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.pixmap_label.resize(200, 50)
        self.pixmap_label.setAlignment(Qt.AlignCenter)

        # qimage = QImage(self.images[0], self.images[0].shape[1], self.images[0].shape[0],
        #                 QImage.Format_RGB888)
        # pixmap = QPixmap(qimage)
        # self.pixmap_label.setPixmap(pixmap)
        self.pixmap_label.move(self.pos1[0],self.pos1[1])
        self.pixmap_label.show()


    def initUI(self):
        self.setWindowTitle('My First Application')
        message = "{0}     {1}".format("Ready",self.now.toString(Qt.DefaultLocaleLongDate))
        self.label()
        self.statusBar().showMessage(message)
        self.setWindowTitle('Statusbar')
        self.move(300, 300)
        self.resize(400, 500)
        self.center()
        self.show()


    # def mouseMoveEvent(self, event):
    #
    #     now = QDate.currentDate()
    #     message = "{0}     {1}     Mouse 위치 ; x={2},y={3}, global={4},{5}".\
    #         format("Ready",now.toString(Qt.DefaultLocaleLongDate), event.x(), event.y(), event.globalX(), event.globalY())
    #
    #     self.statusBar().showMessage(message)

    def mousePressEvent(self, event):
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        self.imageset()
        self.mousePR = True
        message = "{0}     {1}     Mouse 위치 ; x={2},y={3}, global={4},{5}". \
                    format("누름",self.now.toString(Qt.DefaultLocaleLongDate), event.x(), event.y(), event.globalX(), event.globalY())
        self.statusBar().showMessage(message)
        self.update()

    def mouseReleaseEvent(self, event):
        self.pos1[0], self.pos1[1] = event.pos().x(), event.pos().y()
        self.mousePR = False
        message = "{0}     {1}     Mouse 위치 ; x={2},y={3}, global={4},{5}". \
            format("땜", self.now.toString(Qt.DefaultLocaleLongDate), event.x(), event.y(), event.globalX(),
                   event.globalY())
        self.statusBar().showMessage(message)
        self.pixmap_label.deleteLater()
        self.pixmap_label = None
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
        line_edit = QLineEdit(self.centralWidget)
        lbl_red.setStyleSheet("color: black;"
                                  "border-style: solid;"
                                  "border-width: 2px;"
                                  "border-color: #FA8072;"
                                  "border-radius: 3px")
        lbl_red.setText("뀨ㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠㅠ")
        lbl_green.setStyleSheet("color: green;"
                                    "background-color: #7FFFD4")

        lbl_blue.setStyleSheet("color: blue;"
                                   "background-color: #87CEFA;"
                                   "border-style: dashed;"
                                   "border-width: 3px;"
                                   "border-color: #1E90FF")

        vbox = QVBoxLayout(self.centralWidget)

        lbl_red.lower()
        lbl_green.lower()
        lbl_blue.lower()
        line_edit.lower()

        vbox.addWidget(lbl_red)
        vbox.addWidget(lbl_green)
        vbox.addWidget(lbl_blue)
        vbox.addWidget(line_edit)
        # self.imageset()

        self.setCentralWidget(self.centralWidget)

    # def paintEvent(self, event):
    #     if self.pos1 != [0, 0]:
    #
    #         qp = QPainter(self.centralWidget)
    #
    #         qp.begin(self)
    #         self.drawRectangles(qp)
    #         qp.end()
    #
    # def drawRectangles(self,qp):
    #     if self.mousePR ==True:
    #         col = QColor(0, 0, 0)
    #         col.setNamedColor('#d4d4d4')
    #         qp.setPen(col)
    #
    #         qp.setBrush(QColor(200, 0, 0))
    #         qp.drawRect(self.pos1[0], self.pos1[1], 90, 30)
    #
    #         qp.setBrush(QColor(255, 80, 0, 160))
    #         qp.drawRect(self.pos1[0]+110, self.pos1[1], 90, 30)
    #
    #         qp.setBrush(QColor(25, 0, 90, 200))
    #         qp.drawRect(self.pos1[0]+220, self.pos1[1], 90, 30)
    #
    #
    #     else:
    #         qp.eraseRect(self.pos1[0], self.pos1[1], 500, 40)





if __name__ == '__main__':

    app = QApplication(sys.argv)
    windowapp = MainWindow()
    filt = Filter()


    sys.exit(app.exec_())