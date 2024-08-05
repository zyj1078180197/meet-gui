from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.task.ConfigCard import ConfigCard
from meet.util.Class import getClassByName


class TaskCard(ConfigCard):
    def __init__(self, task, parent=None):
        super().__init__(task, parent=parent)
        task = TaskButtons(self, task)
        self.addWidget(task)


class TaskButtons(QWidget):
    def __init__(self, parent, task):
        super().__init__(parent=parent)
        self.task = task
        self.taskBase = getClassByName(task.get("moduleName"), task.get("className"))()
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)  # Set the spacing between widgets
        self.editButton = PushButton(FluentIcon.EDIT, "编辑", self)
        self.editButton.clicked.connect(self.editClicked)

        self.startButton = PushButton(FluentIcon.PLAY, "开始", self)
        self.startButton.clicked.connect(self.startClicked)

        self.stopButton = PushButton(FluentIcon.CLOSE, "停止", self)
        self.stopButton.clicked.connect(self.stopClicked)

        self.pauseButton = PushButton(FluentIcon.PAUSE, "暂停", self)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.layout.addWidget(self.editButton)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.pauseButton)

    def startClicked(self):
        pass

    def stopClicked(self):
        pass

    def pauseClicked(self):
        pass

    def editClicked(self, task):
        pass
