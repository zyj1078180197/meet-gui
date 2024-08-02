from PySide6.QtCore import Signal

from meet.gui.widget.task.TaskCard import TaskCard
from meet.gui.widget.task.TaskTab import TaskTab
from meet.task.BaseTask import BaseTask


class FixedTaskTab(TaskTab):
    taskTabChange = Signal(BaseTask)

    def __init__(self):
        super().__init__()
        taskCard = TaskCard()
        self.addWidget(taskCard)
        self.setObjectName("任务")
        taskCard2 = TaskCard()
        self.addWidget(taskCard2)
        taskCard3 = TaskCard()
        self.addWidget(taskCard3)
        taskCard4 = TaskCard()
        self.addWidget(taskCard4)
        taskCard5 = TaskCard()
        self.addWidget(taskCard5)
        self.taskTabChange.connect(self.taskTabChanged)

    def taskTabChanged(self, task):
        print(task)
        taskCard = TaskCard()
        self.addWidget(taskCard)
