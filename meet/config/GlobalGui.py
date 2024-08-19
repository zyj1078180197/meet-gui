from PySide6.QtWidgets import QApplication


class GlobalGui:
    def __init__(self):
        self.config: dict | None = None
        self.app: QApplication | None = None
        self.meet = None


globalGui = GlobalGui()
