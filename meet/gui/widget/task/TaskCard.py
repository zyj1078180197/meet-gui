from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.plugin.Communicate import communicate
from meet.gui.widget.task.ConfigCard import ConfigCard, ConfigExpandCard
from meet.task.TaskExecutor import TaskExecutor


class TaskCard(ConfigCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(task, parent=parent)
        baseTask.config = task.get('config')
        baseTask.taskId = task.get("taskId")
        taskButton = TaskButtons(self, task, baseTask)
        self.addWidget(taskButton)


class TaskExpandCard(ConfigExpandCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(task, baseTask, parent=parent)
        task = TaskButtons(self, task, baseTask)
        self.addWidget(task)


class TaskButtons(QWidget):
    def __init__(self, parent, task, baseTask):
        self.baseTask = baseTask
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)  # Set the spacing between widgets
        if isinstance(parent, TaskCard):
            self.editButton = PushButton(FluentIcon.EDIT, "编辑", self)
            self.editButton.clicked.connect(lambda: self.editClicked(task, baseTask))
            self.layout.addWidget(self.editButton)
        if isinstance(parent, TaskExpandCard):
            self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
            self.resetConfig.clicked.connect(self.resetConfigClicked)
            self.layout.addWidget(self.resetConfig)

        self.startButton = PushButton(FluentIcon.PLAY, "开始", self)
        self.startButton.clicked.connect(lambda: self.startClicked(baseTask))

        self.stopButton = PushButton(FluentIcon.POWER_BUTTON, "停止", self)
        self.stopButton.clicked.connect(lambda: self.stopClicked(baseTask))
        self.stopButton.hide()

        self.pauseButton = PushButton(FluentIcon.PAUSE, "暂停", self)
        self.pauseButton.clicked.connect(lambda: self.pauseClicked(baseTask))
        self.pauseButton.hide()
        self.deleteButton = PushButton(FluentIcon.DELETE, "删除", self)
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.pauseButton)
        self.layout.addWidget(self.deleteButton)
        communicate.taskStatusChange.connect(self.taskStatusChanged)

    def startClicked(self, baseTask):
        from meet.task.BaseTask import BaseTask
        baseTask.status = BaseTask.StatusEnum.RUNNING
        if baseTask.type == BaseTask.TaskTypeEnum.FIXED:
            TaskExecutor.submitTask(TaskExecutor.fixedTaskRun, baseTask)
        if baseTask.type == BaseTask.TaskTypeEnum.TRIGGER:
            TaskExecutor.submitTask(TaskExecutor.triggerTaskRun, baseTask)
        self.stopButton.show()
        self.pauseButton.show()
        self.deleteButton.hide()
        self.startButton.hide()
        pass

    def stopClicked(self, baseTask):
        from meet.task.BaseTask import BaseTask
        baseTask.status = BaseTask.StatusEnum.STOPPED
        self.startButton.show()
        self.stopButton.hide()
        self.pauseButton.hide()
        self.deleteButton.show()
        pass

    def pauseClicked(self, baseTask):
        from meet.task.BaseTask import BaseTask
        if self.pauseButton.text() == "暂停":
            baseTask.status = BaseTask.StatusEnum.PAUSED
            self.pauseButton.setIcon(FluentIcon.PLAY)
            self.pauseButton.setText("继续")
        else:
            baseTask.status = BaseTask.StatusEnum.RUNNING
            self.pauseButton.setIcon(FluentIcon.PAUSE)
            self.pauseButton.setText("暂停")
        pass

    def editClicked(self, task, baseTask):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.task.TaskEditTab import TaskEditTab
        # 添加新的页面，用于处理配置的改变
        page = globalGui.meet.window.editPageDict.get("编辑任务:" + str(task.get("taskId")))
        if page is None:
            page = TaskEditTab(task, baseTask)
            page.setObjectName("编辑任务:" + str(task.get("taskId")))
        globalGui.meet.openEditPage(page, "编辑任务:" + str(task.get("taskId")))

    def resetConfigClicked(self):
        pass

    def taskStatusChanged(self, baseTask):
        """
        任务结束 按钮的变化
        """
        from meet.task.BaseTask import BaseTask
        if baseTask.taskId == self.baseTask.taskId:
            if baseTask.status == BaseTask.StatusEnum.STOPPED:
                self.startButton.show()
                self.stopButton.hide()
                self.pauseButton.hide()
                self.deleteButton.show()
