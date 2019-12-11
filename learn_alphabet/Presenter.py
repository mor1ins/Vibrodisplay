from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from Model import Vector


class Presenter(object):
    def __init__(self, demo_view, demo_model):
        self.model = demo_model
        self.view = demo_view

        self.view.keySpacePressed.connect(self.start_game)
        self.view.keyPressed.connect(self.model.test)
        self.model.updateView.connect(self.view.update_field)
        self.model.gameOverSignal.connect(self.stop_game)
        self.view.show()

    def start_game(self):
        self.view.clear_display()
        self.model.start_game()

    def stop_game(self):
        self.view.display_game_over()
