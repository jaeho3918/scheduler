import sys


from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QDesktopWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import QDate, Qt


class Formwidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        lbl_red = QLabel('Red')
        lbl_green = QLabel('Green')
        lbl_blue = QLabel('Blue')
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

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(lbl_red)
        self.vbox.addWidget(lbl_green)
        self.vbox.addWidget(lbl_blue)
        self.setLayout(self.vbox)

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_layout)
        self.setWindowTitle('My First Application')
        now = QDate.currentDate()
        message = "{0}     {1}".format("Ready",now.toString(Qt.DefaultLocaleLongDate))

        self.statusBar().showMessage(message)
        self.setWindowTitle('Statusbar')
        self.move(300, 300)
        self.resize(400, 200)
        self.center()

        lbl_red = QLabel('Red')
        lbl_green = QLabel('Green')
        lbl_blue = QLabel('Blue')
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

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_red)
        vbox.addWidget(lbl_green)
        vbox.addWidget(lbl_blue)
        self.setLayout(vbox)


    def center(self):
        framePos = self.frameGeometry()
        centerPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(centerPos)
        self.move(framePos.topLeft())


if __name__ == '__main__':

    app = QApplication(sys.argv)
    windowapp = MyApp()
    windowapp.show()

    sys.exit(app.exec_())