from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QImage, QColor, QPixmap

from Model import Pixel
from config import Config


class View(QtWidgets.QWidget):
    keyPressed = QtCore.pyqtSignal(QtCore.Qt.Key, name="keyPressed")
    keySpacePressed = QtCore.pyqtSignal(name="keySpacePressed")

    def __init__(self, parent=None):
        super().__init__(parent)

    def update_field(self, old, new):
        pass

    def display_game_over(self):
        pass

    def clear_display(self):
        pass


class QtVirtualDisplay(View):
    width, height = Config.WIDTH, Config.HEIGHT
    field = QImage(width, height, QImage.Format_RGB16)

    def __init__(self, parent=None):
        super().__init__()

        self.image_view = QtWidgets.QLabel()
        self.image_view.setGeometry(0, 0, self.width * 100, self.height * 100)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.image_view, 1, 1)

        self.setLayout(layout)
        self.clear_display()

    def clear_display(self):
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
        if event.key() == QtCore.Qt.Key_Space:
            self.keySpacePressed.emit()
        else:
            self.keyPressed.emit(event.key())

    def display_game_over(self):
        self.clear_display()
        #
        # offset = (1, 1)
        #
        # end = [
        #     (0, 0), (1, 0), (2, 0),     (4, 0), (5, 0), (6, 0),
        #     (0, 1),                     (4, 1),         (6, 1),
        #     (0, 2),         (2, 2),     (4, 2),         (6, 2),
        #     (0, 3),         (2, 3),     (4, 3),         (6, 3),
        #     (0, 4), (1, 4), (2, 4),     (4, 4), (5, 4), (6, 4),
        # ]

        # for i in range(len(end)):
        #     end[i] = (end[i][0] + offset[0], end[i][1] + offset[1])

        # self.update_field([], end)
