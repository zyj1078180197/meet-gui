from PySide6.QtCore import QObject, Signal

from meet.task.BaseTask import BaseTask


class Communicate(QObject):
    """
    自定义信号
    """
    # 主题切换信号
    themeChange = Signal()


communicate = Communicate()
