from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import PushButton, FluentIcon, MessageBox

from meet.gui.plugin.Communicate import communicate
from meet.gui.widget.OperationButton import OperationButton
from meet.gui.widget.task.ConfigCard import ConfigCard, ConfigExpandCard
from meet.task.TaskExecutor import TaskExecutor
from meet.util.MessageTips import showSuccess
from meet.util.Task import Task


class TaskCard(ConfigCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(task, parent=parent)
        self.parentTab = parent
        if task.get('config') is None or task.get('config') == {}:
            task['config'] = baseTask.defaultConfig
            Task.updateTask(task)
        else:
            task['config'] = baseTask.defaultConfig | task.get('config')
            Task.updateTask(task)
        baseTask.config = task.get('config')
        baseTask.taskId = task.get("taskId")
        baseTask.configPath = task.get("configPath")
        taskButton = TaskButtons(self, task, baseTask)
        self.clicked.connect(lambda: TaskButtons.editClicked(task, baseTask))
        self.addWidget(taskButton)


class TaskExpandCard(ConfigExpandCard):
    def __init__(self, task, baseTask, parent=None):
        super().__init__(task, baseTask, parent=parent)
        self.parentTab = parent
        task = TaskButtons(self, task, baseTask)
        self.addWidget(task)


class TaskButtons(QWidget):
    def __init__(self, parent, task, baseTask):
        self.baseTask = baseTask
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)  # Set the spacing between widgets
        self.copyButton = OperationButton(FluentIcon.COPY, "复制", self)
        self.copyButton.clicked.connect(lambda: self.copyClicked(task, parent))
        self.layout.addWidget(self.copyButton)
        if isinstance(parent, TaskCard):
            self.editButton = PushButton(FluentIcon.EDIT, "编辑", self)
            self.editButton.clicked.connect(lambda: self.editClicked(task, baseTask))
            self.layout.addWidget(self.editButton)
        if isinstance(parent, TaskExpandCard):
            self.resetConfig = PushButton(FluentIcon.CANCEL, "重置", self)
            self.resetConfig.clicked.connect(lambda: self.resetConfigClicked(parent))
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
        self.deleteButton.clicked.connect(lambda: self.deleteClicked(baseTask, parent))
        self.layout.addWidget(self.startButton)
        self.layout.addWidget(self.stopButton)
        self.layout.addWidget(self.pauseButton)
        self.layout.addWidget(self.deleteButton)
        communicate.taskStatusChange.connect(self.taskStatusChanged)

    @staticmethod
    def copyClicked(task, parent):
        taskCopy = Task.addTasks(task)
        from meet.util.Class import getClassByName
        baseTask = getClassByName(taskCopy.get("moduleName"), taskCopy.get("className"))()
        from meet.gui.widget.task.FixedTaskTab import FixedTaskTab
        if taskCopy.get("showStyle") == FixedTaskTab.ShowStyle.EXPAND.value:
            taskExpandCard = TaskExpandCard(taskCopy, baseTask, parent.parentTab)
            parent.parentTab.insertWidget(taskExpandCard, parent.parentTab.getWidgetIndex(parent) + 1)
        else:
            taskCard = TaskCard(taskCopy, baseTask, parent.parentTab)
            parent.parentTab.insertWidget(taskCard, parent.parentTab.getWidgetIndex(parent) + 1)
        showSuccess("复制成功")

    @staticmethod
    def deleteClicked(baseTask, parent):
        from meet.config.GlobalGui import globalGui
        m = MessageBox("消息", "确认删除?", globalGui.meet.window)
        m.yesButton.setText("确定")
        m.cancelButton.setText("取消")
        if m.exec():
            if Task.deleteTask(baseTask):
                parent.close()
                parent.deleteLater()
        m.close()
        m.deleteLater()

    def startClicked(self, baseTask):
        from meet.task.BaseTask import BaseTask
        baseTask.status = BaseTask.StatusEnum.RUNNING
        baseTask.executeNumber = baseTask.defaultExecuteNumber
        if baseTask.type == BaseTask.TaskTypeEnum.FIXED:
            TaskExecutor.submitTask(TaskExecutor.fixedTaskRun, baseTask)
        if baseTask.type == BaseTask.TaskTypeEnum.TRIGGER:
            TaskExecutor.submitTask(TaskExecutor.triggerTaskRun, baseTask)
        self.stopButton.show()
        self.pauseButton.show()
        self.pauseButton.setText("暂停")
        self.pauseButton.setIcon(FluentIcon.PAUSE)
        self.deleteButton.hide()
        self.startButton.hide()
        showSuccess(baseTask.className + "-" + str(baseTask.taskId) + "任务已开始")

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
            showSuccess(baseTask.className + "-" + str(baseTask.taskId) + "任务已暂停")
        else:
            baseTask.status = BaseTask.StatusEnum.RUNNING
            self.pauseButton.setIcon(FluentIcon.PAUSE)
            self.pauseButton.setText("暂停")
            showSuccess(baseTask.className + "-" + str(baseTask.taskId) + "任务已继续")
        pass

    @staticmethod
    def editClicked(task, baseTask):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.task.TaskEditTab import TaskEditTab
        # 添加新的页面，用于处理配置的改变
        page = globalGui.meet.window.editPageDict.get("编辑任务:" + str(task.get("taskId")))
        if page is None:
            page = TaskEditTab(task, baseTask)
            page.setObjectName("编辑任务:" + str(task.get("taskId")))
        globalGui.meet.openEditPage(page, "编辑任务:" + str(task.get("taskId")))

    @staticmethod
    def resetConfigClicked(parent: TaskExpandCard = None):
        parent.resetConfigValue()
        showSuccess("重置成功")

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
                showSuccess(baseTask.className + "-" + str(baseTask.taskId) + "任务已停止")
