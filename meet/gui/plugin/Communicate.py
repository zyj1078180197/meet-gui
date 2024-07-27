from PySide6.QtCore import QObject, Signal


class Communicate(QObject):
    """
    自定义信号
    """
    # 浏览历史记录改变
    browserHistoryChange = Signal()


communicate = Communicate()
