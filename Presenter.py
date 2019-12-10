from PyQt5.QtCore import QTimer


class Presenter(object):
    def __init__(self, demo_view, demo_model):
        self.model = demo_model
        self.view = demo_view

        self.view.buttonClickEvent.connect(self.model.move_platform)
        self.model.gameOverSignal.connect(self.stop_game)

        self.view.show()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_display)
        self.timer.start(5)

    def update_display(self):
        self.model.update_display()
        self.view.update_field(self.model.field)
        self.view.update_display()

    def stop_game(self):
        self.timer.stop()


