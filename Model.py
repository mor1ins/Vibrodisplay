from random import randint

import PyQt5.QtCore as QtCore
from config import Config
from collections import namedtuple
import copy


class Pixel(QtCore.QObject):
    changedPosition = QtCore.pyqtSignal(list, list, name="changedPosition")

    def __init__(self, x, y):
        super().__init__()

        self.x = x
        self.y = y

    def set_position(self, x, y):
        old_pixels = copy.deepcopy(self.get_pixels())
        self.x, self.y = x, y
        self.changedPosition.emit(old_pixels, self.get_pixels())

    def get_position(self):
        return self.x, self.y

    def get_pixels(self):
        return [self.get_position()]


class Ball(Pixel):
    gameOverSignal = QtCore.pyqtSignal(name="gameOverSignal")

    def __init__(self, width, height, platforms):
        super().__init__(int(width / 2), int(height / 2))
        self.width = width
        self.height = height
        self.platforms = platforms
        self.to_start_point()

        self.current_direct = Direct.get_zero_direct()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.move)

    def to_start_point(self):
        self.set_position(int(self.width / 2), int(self.height / 2))

    def start(self, direct, speed):
        self.current_direct = direct
        self.timer.start(speed)

    def reply(self):
        ball = Ball(self.width, self.height, self.platforms)
        ball.set_position(self.x, self.y)
        return ball

    def apply_direction(self, direct):
        x, y = direct.apply(*self.get_position())
        self.set_position(x, y)
        return self

    def future(self):
        return self.reply().apply_direction(self.current_direct)

    def move(self):
        if self.x == 0:
            self.timer.stop()
            return

        future_ball = self.future()
        x, y = future_ball.get_position()

        first = list(filter(
            lambda platform: platform.intersect(x, y), self.platforms))
        second = list(filter(
            lambda platform: platform.intersect(x - self.current_direct.shift.x, y),
            self.platforms))
        third = list(filter(
            lambda platform: platform.intersect(x, y - self.current_direct.shift.y),
            self.platforms))

        if len(first) > 0 and len(second) == 0 and len(third) == 0:
            self.current_direct = self.current_direct.opposite()
        else:
            for platform in set(first + second + third):
                self.current_direct = platform.reflect(self.current_direct)

        self.apply_direction(self.current_direct)


class Direct:
    def __init__(self, x, y):
        self.shift = namedtuple("shift", ["x", "y"])
        self.shift.x, self.shift.y = x, y

    def opposite(self):
        return Direct(self.shift.x * (-1), self.shift.y * (-1))

    def reflect_x(self):
        self.shift.x *= -1
        return self

    def reflect_y(self):
        self.shift.y *= -1
        return self

    def reflect(self):
        self.reflect_x()
        self.reflect_y()

    def apply(self, x, y):
        return x + self.shift.x, y + self.shift.y

    def __add__(self, other):
        return Direct(self.shift.x + other.shift.x, self.shift.y + other.shift.y)

    def __eq__(self, other):
        return self.shift.x == other.shift.x or self.shift.y == other.shift.y

    @staticmethod
    def get_zero_direct():
        return Direct(0, -1)

    @staticmethod
    def get_up_direct():
        return Direct(0, -1)

    @staticmethod
    def get_down_direct():
        return Direct(0, 1)

    @staticmethod
    def get_right_direct():
        return Direct(1, 0)

    @staticmethod
    def get_left_direct():
        return Direct(-1, 0)

    @staticmethod
    def get_up_right_direct():
        return Direct.get_up_direct() + Direct.get_right_direct()

    @staticmethod
    def get_up_left_direct():
        return Direct.get_up_direct() + Direct.get_left_direct()

    @staticmethod
    def get_down_right_direct():
        return Direct.get_down_direct() + Direct.get_right_direct()

    @staticmethod
    def get_down_left_direct():
        return Direct.get_down_direct() + Direct.get_left_direct()

    @staticmethod
    def get_random_diagonal_direction():
        directions = [
            Direct.get_up_right_direct(), Direct.get_up_left_direct(),
            Direct.get_down_right_direct(), Direct.get_down_left_direct(),
        ]

        return directions[randint(0, len(directions) - 1)]


class Platform(QtCore.QObject):
    changedPosition = QtCore.pyqtSignal(list, list, name="changedPosition")

    def __init__(self, head_x, head_y, direction: Direct, platform_width=1):
        super().__init__()

        self.platform_width = platform_width
        self.__direction = direction

        pixels = [(head_x, head_y)]
        for i in range(platform_width - 1):
            pixels.append(direction.apply(*pixels[i]))

        self.pixels = []
        for pixel in pixels:
            self.pixels.append(Pixel(*pixel))

    def get_pixels(self):
        return [pixel.get_position() for pixel in self.pixels]

    def intersect(self, x, y):
        inner = len(list(filter(lambda p: p.x == x and p.y == y, self.pixels))) > 0

        return len(list(filter(lambda p: p.x == x and p.y == y, self.pixels))) > 0

    def move(self, direction: Direct):
        old_pixels = copy.deepcopy(self.get_pixels())
        self.pixels = [Pixel(*direction.apply(*pixel.get_position())) for pixel in self.pixels]
        self.changedPosition.emit(old_pixels, self.get_pixels())

    def is_horizontal(self):
        return self.__direction == Direct.get_left_direct() or self.__direction == Direct.get_right_direct()

    def reflect(self, direct):
        is_horizontal = self.is_horizontal()
        return direct.reflect_y() if is_horizontal else direct.reflect_x()


class Model(QtCore.QObject):
    gameOverSignal = QtCore.pyqtSignal(name="gameOverSignal")
    updateView = QtCore.pyqtSignal(list, list, name="updateView")

    def __init__(self):
        super().__init__()
        self.ready = False
        self.height = Config.HEIGHT
        self.width = Config.WIDTH

        self.gamer_platform = Platform(0, int(self.height / 2), Direct.get_down_direct())

        self.right_wall = Platform(self.width, 0, Direct.get_down_direct(), self.height)
        self.up_wall = Platform(0, -1, Direct.get_right_direct(), self.width)
        self.down_wall = Platform(0, self.height, Direct.get_right_direct(), self.width)

        self.platforms = [self.gamer_platform, self.right_wall, self.up_wall, self.down_wall]
        self.ball = Ball(self.width, self.height, self.platforms)

        self.gamer_platform.changedPosition.connect(self.update_view)
        self.ball.changedPosition.connect(self.update_view)
        self.ball.gameOverSignal.connect(lambda: self.gameOverSignal.emit())
        self.ready = True

    def start_game(self):
        if self.ready:
            self.ball.to_start_point()

            pixels = self.ball.get_pixels() + self.gamer_platform.get_pixels()
            self.update_view([], pixels)
            self.ball.start(Direct.get_random_diagonal_direction(), 500)

    def update_view(self, old_pixels, new_pixels):
        self.updateView.emit(old_pixels, new_pixels)
