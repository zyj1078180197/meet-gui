from PySide6.QtCore import QObject, Signal

from meet.task.BaseTask import BaseTask


class Communicate(QObject):
    """
    自定义信号
    """
    # 浏览历史记录改变
    browserHistoryChange = Signal()
    themeChange = Signal()


communicate = Communicate()
