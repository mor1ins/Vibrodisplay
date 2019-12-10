from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QColor, QPixmap

from Model import Pixel
from config import Config


class View(QtWidgets.QWidget):
    keyUpPressed = QtCore.pyqtSignal(name="keyUpPressed")
    keyDownPressed = QtCore.pyqtSignal(name="keyDownPressed")
    ready = QtCore.pyqtSignal(name="ready")

    width, height = Config.WIDTH, Config.HEIGHT
    field = QImage(width, height, QImage.Format_RGB16)

    def __init__(self, parent=None):
        super(View, self).__init__(parent)

        self.image_view = QtWidgets.QLabel()
        self.image_view.setGeometry(0, 0, self.width * 100, self.height * 100)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.image_view, 1, 1)

        self.setLayout(layout)
        pixels = []
        for x in range(self.field.width()):
            for y in range(self.field.height()):
                pixels.append((x, y))

        self.update_field(pixels, [])

    def fill(self, pixels, color):
        for x, y in pixels:
            self.field.setPixel(x, y, QColor(*color).rgb())

    def update_field(self, old, new):
        self.fill(old, (0, 0, 0))
        self.fill(new, (255, 255, 255))
        self.update_display()

    def update_display(self):
        pixel_map = QPixmap.fromImage(self.field)
        self.image_view.setPixmap(pixel_map)
        self.image_view.setAlignment(QtCore.Qt.AlignCenter)
        self.image_view.setScaledContents(True)
        self.image_view.setMinimumSize(self.width * 50, self.height * 50)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Up:
            self.keyUpPressed.emit()
        elif event.key() == QtCore.Qt.Key_Down:
            self.keyDownPressed.emit()
        elif event.key() == QtCore.Qt.Key_Space:
            self.ready.emit()





