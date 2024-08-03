from PySide6.QtWidgets import QApplication

from meet.gui.widget.task.FixedTaskTab import FixedTaskTab


class GlobalGui:
    def __init__(self):
        self.fixedTaskTab: FixedTaskTab | None = None
        self.config: dict | None = None
        self.app: QApplication | None = None
        self.meet = None


globalGui = GlobalGui()
