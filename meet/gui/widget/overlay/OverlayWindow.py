from PySide6.QtCore import Qt

from meet.gui.widget.debug.FrameWidget import FrameWidget


class OverlayWindow(FrameWidget):
    def __init__(self):
        super().__init__()
        # 设置部件背景为半透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 确保部件能够正确接收鼠标事件
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

        # 设置窗口标志，使窗口无边框、始终置顶、作为工具窗口，并支持透明输入
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.WindowTransparentForInput)

    def updateOverlay(self, visible, x, y, width, height, scaling):
        # 如果可见，则更新窗口位置和尺寸
        if visible:
            self.setGeometry(x / scaling, y / scaling, width / scaling, height / scaling)
        # 如果可见并且当前不可见，则显示窗口
        if visible and not self.isVisible():
            self.show()
            return
        # 如果不可见并且当前可见，则隐藏窗口
        if not visible and self.isVisible():
            self.hide()
