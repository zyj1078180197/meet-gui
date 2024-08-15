from enum import Enum

from meet.gui.widget.task.TaskCard import TaskExpandCard, TaskCard
from meet.gui.widget.task.TaskTab import TaskTab
from meet.task.TaskExecutor import TaskExecutor
from meet.util.Class import getClassByName


class TriggerTaskTab(TaskTab):
    class ShowStyle(Enum):
        NORMAL = 'Normal'
        EXPAND = 'Expand'

    def __init__(self, parent=None):
        super().__init__(parent)
        for taskList in TaskExecutor.triggerTaskList:
            for task in taskList:
                baseTask = getClassByName(task.get("moduleName"), task.get("className"))()
                if task.get("showStyle") == TriggerTaskTab.ShowStyle.EXPAND.value:
                    taskExpandCard = TaskExpandCard(task, baseTask, self)
                    self.addWidget(taskExpandCard)
                else:
                    taskCard = TaskCard(task, baseTask, self)
                    self.addWidget(taskCard)
        self.setObjectName("触发")

    def closeEvent(self, event):
        self.deleteLater()
        event.accept()
