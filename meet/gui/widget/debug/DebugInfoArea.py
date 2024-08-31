from datetime import datetime
from fileinput import close

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QTextCharFormat, QColor, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy

from meet.gui.plugin.Communicate import communicate

log_levels = {
    'INFO': Qt.GlobalColor.darkGreen,
    'WARN': Qt.GlobalColor.darkYellow,
    'ERROR': Qt.GlobalColor.darkRed,
}


class DebugInfoArea(QWidget):

    def __init__(self):
        super().__init__()
        # 设置部件背景为半透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowTitle('Debug Info')
        from meet.config.Config import Config
        from meet.config.GlobalGui import globalGui
        config = Config.loadConfig(globalGui.config)
        from meet.util.Path import getPathRelativeToExe
        appIcon = getPathRelativeToExe(config.get("appIcon", "resource\\logo.png"))
        self.setWindowIcon(QIcon(appIcon))

        # 确保部件能够正确接收鼠标事件
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent)

        # 设置窗口标志，使窗口无边框、始终置顶、作为工具窗口，并支持透明输入
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint)
        # 创建一个中心小部件和布局
        layout = QVBoxLayout(self)

        # 创建一个文本编辑区，用于显示日志
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        # 设置透明背景
        self.log_text_edit.setStyleSheet("background-color: rgba(0, 0, 0, 25);")
        layout.addWidget(self.log_text_edit)

        self.hLayout = QHBoxLayout(self)
        closeButton = QPushButton("关闭")
        closeButton.clicked.connect(self.hide)
        clearButton = QPushButton("清空")
        clearButton.clicked.connect(self.log_text_edit.clear)
        # self.hLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        self.hLayout.addWidget(closeButton)
        self.hLayout.addWidget(clearButton)
        # self.hLayout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        layout.addLayout(self.hLayout)

        self.setGeometry(0, 680, 400, 400)
        communicate.logMsg.connect(self.addLog)

    @Slot()
    def addLog(self, level, message):
        # 日志级别和对应的颜色
        # 设置日志颜色
        color = log_levels.get(level, Qt.GlobalColor.black)
        self.setLogColor(color)

        # 在文本编辑区中添加日志
        self.log_text_edit.append(f"[{level}] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {message}")
        # 文本超过1000行时
        if self.log_text_edit.document().lineCount() > 1000:
            self.log_text_edit.clear()

        # 确保滚动条在最新消息的位置
        self.scrollToBottom()

    def setLogColor(self, color):
        text_format = QTextCharFormat()
        text_format.setForeground(QColor(color))
        self.log_text_edit.setCurrentCharFormat(text_format)

    def scrollToBottom(self):
        # 获取垂直滚动条
        scrollbar = self.log_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
