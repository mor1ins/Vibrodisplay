
from Presenter import Presenter
from Model import Model
from View import View

from PyQt5 import QtWidgets

import sys


class Demo(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)

        self.window = QtWidgets.QMainWindow()

        self.demo_view = View()
        self.demo_model = Model()

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.demo_view, 1, 1)
        self.setLayout(layout)
        self.show()

        self.presenter = Presenter(self.demo_view, self.demo_model)
        self.setWindowTitle("Ping Pong")


def qapp():
    if QtWidgets.QApplication.instance():
        _app = QtWidgets.QApplication.instance()
    else:
        _app = QtWidgets.QApplication(sys.argv)
    return _app


if __name__ == "__main__":
    app = qapp()
    window = Demo()
    app.exec_()
