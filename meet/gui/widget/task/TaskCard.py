from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.task.ConfigCard import ConfigCard


class TaskCard(ConfigCard):
    def __init__(self):
        super().__init__()
        task = TaskButtons(11)
        self.addWidget(task)


class TaskButtons(QWidget):
    def __init__(self, task, OKIcon=None):
        super().__init__()
        self.task = task
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)  # Set the spacing between widgets

        self.startButton = PushButton(FluentIcon.PLAY, "开始", self)
        self.startButton.clicked.connect(self.startClicked)

        self.stopButton = PushButton(FluentIcon.CLOSE, "停止", self)
        self.stopButton.clicked.connect(self.stopClicked)

        self.pauseButton = PushButton(FluentIcon.PAUSE, "暂停", self)
        self.pauseButton.clicked.connect(self.pauseClicked)
        # Add buttons to the layout
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.pauseButton)

    def startClicked(self):
        pass

    def stopClicked(self):
        pass

    def pauseClicked(self):
        pass