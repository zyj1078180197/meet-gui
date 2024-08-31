from PySide6.QtCore import QObject, Signal

from meet.task.BaseTask import BaseTask


class Communicate(QObject):
    """
    自定义信号
    """
    # 浏览历史记录改变
    browserHistoryChange = Signal()
    themeChange = Signal()
    # 任务状态改变
    taskStatusChange = Signal(BaseTask)
    logMsg = Signal(str, str)


communicate = Communicate()
