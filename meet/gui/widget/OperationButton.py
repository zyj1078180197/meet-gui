from qfluentwidgets import PushButton


class OperationButton(PushButton):

    def __init__(self, icon, text, parent=None):
        super().__init__(parent)
        self.leaveKwargs = None
        self.enterKwargs = None
        self.leaveArgs = None
        self.enterArgs = None
        self.leaveEventHandle = None
        self.enterEventHandle = None
        self.setIcon(icon)
        self.setText(text)

    def addEnterEventHandle(self, handler, *args, **kwargs):
        self.enterEventHandle = handler
        self.enterArgs = args
        self.enterKwargs = kwargs

    def addLeaveEventHandle(self, handler, *args, **kwargs):
        self.leaveEventHandle = handler
        self.leaveArgs = args
        self.leaveKwargs = kwargs

    def enterEvent(self, e):
        if self.enterEventHandle is None:
            return
        self.enterEventHandle(*self.enterArgs, **self.enterKwargs)

    def leaveEvent(self, e):
        if self.leaveEventHandle is None:
            return
        self.leaveEventHandle(*self.leaveArgs, **self.leaveKwargs)

    def closeEvent(self, event):
        self.deleteLater()
