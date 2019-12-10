from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from Model import Direct


class Presenter(object):
    def __init__(self, demo_view, demo_model):
        self.model = demo_model
        self.view = demo_view

        self.view.keyUpPressed.connect(
            lambda: self.model.gamer_platform.move(Direct.get_up_direct())
        )
        self.view.keyDownPressed.connect(
            lambda: self.model.gamer_platform.move(Direct.get_down_direct())
        )

        self.model.updateView.connect(self.view.update_field)
        self.model.gameOverSignal.connect(self.stop_game)

        self.view.ready.connect(self.model.start_game)
        self.view.show()

    def stop_game(self):
        pass
