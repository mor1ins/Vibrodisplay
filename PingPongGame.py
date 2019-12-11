
from Presenter import Presenter
from Model import Model
from View import View, QtVirtualDisplay

from PyQt5 import QtWidgets

import sys


class PingPongGame(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(PingPongGame, self).__init__(parent)

        self.window = QtWidgets.QMainWindow()

        self.demo_view = QtVirtualDisplay()
        self.demo_model = Model()

        self.presenter = Presenter(self.demo_view, self.demo_model)


def qapp():
    if QtWidgets.QApplication.instance():
        _app = QtWidgets.QApplication.instance()
    else:
        _app = QtWidgets.QApplication(sys.argv)
    return _app


if __name__ == "__main__":
    app = qapp()
    window = PingPongGame()
    app.exec_()
