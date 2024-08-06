from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.task.ConfigCard import ConfigCard, ConfigExpandCard


class TaskCard(ConfigCard):
    def __init__(self, task, taskBase, parent=None):
        super().__init__(task, parent=parent)
        task = TaskButtons(self, task, taskBase)
        self.addWidget(task)


class TaskExpandCard(ConfigExpandCard):
    def __init__(self, task, taskBase, parent=None):
        super().__init__(task, taskBase, parent=parent)
        task = TaskButtons(self, task, taskBase)
        self.addWidget(task)


class TaskButtons(QWidget):
    def __init__(self, parent, task, taskBase):
        super().__init__(parent=parent)
        self.task = task
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)  # Set the spacing between widgets
        if isinstance(parent, TaskCard):
            self.editButton = PushButton(FluentIcon.EDIT, "编辑", self)
            self.editButton.clicked.connect(self.editClicked)
            self.layout.addWidget(self.editButton)
        if isinstance(parent, TaskExpandCard):
            self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
            self.resetConfig.clicked.connect(self.resetConfigClicked)
            self.layout.addWidget(self.resetConfig)

        self.startButton = PushButton(FluentIcon.PLAY, "开始", self)
        self.startButton.clicked.connect(self.startClicked)

        self.stopButton = PushButton(FluentIcon.POWER_BUTTON, "停止", self)
        self.stopButton.clicked.connect(self.stopClicked)
        self.stopButton.hide()

        self.pauseButton = PushButton(FluentIcon.PAUSE, "暂停", self)
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.pauseButton.hide()
        self.deleteButton = PushButton(FluentIcon.DELETE, "删除", self)
        self.deleteButton.clicked.connect(self.editClicked)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.pauseButton)
        self.layout.addWidget(self.deleteButton)

    def startClicked(self):
        self.stopButton.show()
        self.pauseButton.show()
        self.deleteButton.hide()
        self.startButton.hide()
        pass

    def stopClicked(self):
        self.startButton.show()
        self.stopButton.hide()
        self.pauseButton.hide()
        self.deleteButton.show()
        pass

    def pauseClicked(self):
        if self.pauseButton.text() == "暂停":
            self.pauseButton.setIcon(FluentIcon.PLAY)
            self.pauseButton.setText("继续")
        else:
            self.pauseButton.setIcon(FluentIcon.PAUSE)
            self.pauseButton.setText("暂停")
        pass

    def editClicked(self):
        pass

    def resetConfigClicked(self):
        pass
