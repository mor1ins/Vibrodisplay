from random import randint

import PyQt5.QtCore as QtCore
from config import Config


class Pixel(QtCore.QObject):
    def __init__(self, field, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.field = field

    def display(self):
        self.field[self.x][self.y] = True


class Ball(Pixel):
    gameOverSignal = QtCore.pyqtSignal(name="gameOverSignal")

    def __init__(self, field, width, height):
        super().__init__(field, int(width / 2), int(height / 2))
        self.width = width
        self.height = height

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.move)
        self.directs = [
            (-1, -1), (1, -1),
            (-1,  1), (1,  1),
        ]
        self.current_direct = self.directs[randint(0, len(self.directs) - 1)]
        self.timer.start(500)

    def move(self):
        x, y = self.current_direct

        if self.x == 0 or self.x == self.width - 1:
            self.timer.stop()
            return
        elif self.y == 0 or self.y == self.height - 1:
            self.current_direct = (x, y * (-1))
            x, y = self.current_direct

        if self.field[self.x + x][self.y + y]:
            self.current_direct = (x * (-1), y)
            x, y = self.current_direct

        self.x += x
        self.y += y


class Platform(Pixel):
    def __init__(self, field, x, y, height, platform_width=1):
        super().__init__(field, x, y)
        self.height = height
        self.platform_width = platform_width

    def move(self, direct):
        if direct == QtCore.Qt.Key_Up and self.y > 0:
            self.y -= 1
        elif direct == QtCore.Qt.Key_Down and self.y < self.height - self.platform_width:
            self.y += 1

    def display(self):
        for y in range(self.y, self.y + self.platform_width):
            self.field[self.x][y] = True


class Model(QtCore.QObject):
    gameOverSignal = QtCore.pyqtSignal(name="gameOverSignal")

    def __init__(self):
        super().__init__()
        self.height = Config.HEIGHT
        self.width = Config.WIDTH
        self.field = []
        for _ in range(self.width):
            row = []
            for _ in range(self.height):
                row.append(False)
            self.field.append(row)

        self.gamer_platform = Platform(self.field, 0, int(self.height / 2), self.height, 1)
        self.other_platform = Platform(self.field, self.width - 1, 0, self.height, self.height)
        self.ball = Ball(self.field, self.width, self.height)
        self.ball.gameOverSignal.connect(lambda x: self.gameOverSignal.emit())

        self.clear_field()
        self.gamer_platform.display()

    def clear_field(self):
        for x in range(self.width):
            for y in range(self.height):
                self.field[x][y] = False

    def update_display(self):
        self.clear_field()
        self.gamer_platform.display()
        self.other_platform.display()
        self.ball.display()

    def move_ball(self):
        pass

    def move_platform(self, direct):
        self.gamer_platform.move(direct)
