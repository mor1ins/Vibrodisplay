from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QColor, QPixmap
from config import Config


class View(QtWidgets.QWidget):
    buttonClickEvent = QtCore.pyqtSignal(QtCore.Qt.Key, name="buttonClickEvent")
    width, height = Config.WIDTH, Config.HEIGHT
    field = QImage(width, height, QImage.Format_RGB16)

    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.clear_field()

        self.image_view = QtWidgets.QLabel()
        self.image_view.setGeometry(0, 0, self.width * 100, self.height * 100)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.image_view, 1, 1)

        self.installEventFilter(self)

        self.setLayout(layout)
        self.update_display()
        self.show()

    def clear_field(self):
        for x in range(self.field.width()):
            for y in range(self.field.height()):
                self.field.setPixel(x, y, QColor(0, 0, 0).rgb())

    def update_field(self, field):
        self.clear_field()
        for x in range(len(field)):
            for y in range(len(field[x])):
                if field[x][y]:
                    self.field.setPixel(x, y, QColor(255, 255, 255).rgb())

    def update_display(self):
        pixel_map = QPixmap.fromImage(self.field)
        self.image_view.setPixmap(pixel_map)
        self.image_view.setAlignment(QtCore.Qt.AlignCenter)
        self.image_view.setScaledContents(True)
        self.image_view.setMinimumSize(self.width * 50, self.height * 50)
        self.image_view.show()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up or event.key() == QtCore.Qt.Key_Down:
            self.buttonClickEvent.emit(event.key())





