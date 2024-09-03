import threading

from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, FluentIcon

from meet.executor.task.TaskExecutor import TaskExecutor
from meet.gui.plugin.Communicate import communicate
from meet.gui.widget.task.ConfigCard import ConfigCard, ConfigExpandCard
from meet.util.MessageTips import showSuccess


class TaskCard(ConfigCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(task, parent=parent)
        self.parentTab = parent
        taskButton = TaskButtons(self, task, baseTask)
        self.clicked.connect(lambda: TaskButtons.editClicked(task, baseTask))
        self.addWidget(taskButton)


class TaskExpandCard(ConfigExpandCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(task, baseTask, parent=parent)
        self.parentTab = parent
        taskButton = TaskButtons(self, task, baseTask)
        self.addWidget(taskButton)


class TaskButtons(QWidget):
    def __init__(self, parent, task, baseTask):
        self.stopEvent = None
        self.task = task
        self.menu = None
        self.baseTask = baseTask
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)

        self.startButton = PushButton(FluentIcon.PLAY, "启动", self)
        self.startButton.clicked.connect(lambda: self.startClicked(baseTask))
        self.startButton.show()

        self.stopButton = PushButton(FluentIcon.POWER_BUTTON, "停止", self)
        self.stopButton.clicked.connect(lambda: self.stopClicked(baseTask))
        self.stopButton.hide()

        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        communicate.taskStatusChange.connect(self.taskStatusChanged)

    def startClicked(self, baseTask):
        from meet.executor.task.BaseTask import BaseTask
        baseTask.status = BaseTask.StatusEnum.RUNNING.value
        baseTask.stopEvent = threading.Event()
        TaskExecutor.submitTask(TaskExecutor.taskRun, baseTask)
        self.stopButton.show()
        self.startButton.hide()
        showSuccess("")

    def stopClicked(self, baseTask):
        from meet.executor.task.BaseTask import BaseTask
        baseTask.status = BaseTask.StatusEnum.STOPPED.value
        self.startButton.show()
        self.stopButton.hide()
        baseTask.stopEvent.set()
        pass

    @staticmethod
    def editClicked(task, baseTask):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.task.TaskEditTab import TaskEditTab
        if task.get("config") is None or task.get("config") == {}:
            return
        # 添加新的页面，用于处理配置的改变
        page = globalGui.meet.window.editPageDict.get("编辑任务:" + str(task.get("taskId")))
        if page is None:
            page = TaskEditTab(task, baseTask)
            page.setObjectName("编辑任务:" + str(task.get("taskId")))
        globalGui.meet.openEditPage(page, "编辑任务:" + str(task.get("taskId")))

    def taskStatusChanged(self, baseTask):
        """
        任务结束 按钮的变化
        """
        from meet.executor.task.BaseTask import BaseTask
        if baseTask.taskId == self.baseTask.taskId:
            if baseTask.status == BaseTask.StatusEnum.STOPPED.value:
                self.startButton.show()
                self.stopButton.hide()
