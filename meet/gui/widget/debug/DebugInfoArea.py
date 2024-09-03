from datetime import datetime

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QTextCharFormat, QColor, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

from meet.gui.plugin.Communicate import communicate

logLevels = {
    'INF': Qt.GlobalColor.white,
    'WAR': Qt.GlobalColor.yellow,
    'ERR': Qt.GlobalColor.red,
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
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
            | Qt.WindowType.WindowTransparentForInput
        )
        # 创建一个中心小部件和布局
        layout = QVBoxLayout(self)

        # 创建一个文本编辑区，用于显示日志
        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)
        # 隐藏滚动条
        self.logTextEdit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置透明背景
        self.logTextEdit.setStyleSheet("background-color: rgba(0, 0, 0, 25);")
        layout.addWidget(self.logTextEdit)
        self.setGeometry(20, 780, 400, 300)
        communicate.logMsg.connect(self.addLog)

    @Slot()
    def addLog(self, level, message):
        # 日志级别和对应的颜色
        colorLevel = logLevels.get(level, Qt.GlobalColor.gray)
        colorTime = Qt.GlobalColor.gray
        colorContent = Qt.GlobalColor.white

        # 在文本编辑区中添加日志
        timestamp = datetime.now().strftime('%H:%M:%S')
        logMessage = f"[{timestamp}] [{level}] {message}"
        self.insertColoredText(logMessage, colorLevel, colorTime, colorContent)

        # 文本超过1000行时
        if self.logTextEdit.document().lineCount() > 1000:
            self.logTextEdit.clear()

        # 确保滚动条在最新消息的位置
        self.scrollToBottom()

    def insertColoredText(self, text, colorLevel, colorTime, colorContent):
        cursor = self.logTextEdit.textCursor()
        formatLevel = QTextCharFormat()
        formatLevel.setForeground(QColor(colorLevel))

        formatTime = QTextCharFormat()
        formatTime.setForeground(QColor(colorTime))

        formatContent = QTextCharFormat()
        formatContent.setForeground(QColor(colorContent))

        parts = text.split()
        cursor.beginEditBlock()
        cursor.insertText(parts[0], formatTime)  # 日志级别
        cursor.insertText('  ', formatContent)
        cursor.insertText(parts[1], formatLevel)  # 时间戳
        cursor.insertText('  ', formatContent)
        for part in ''.join(parts[2:]).split("#"):
            if part == "":
                continue
            formatContentPart = QTextCharFormat()
            #第一个字符判断
            if part[0] =="r":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.red))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            if part[0] =="g":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.green))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            if part[0] =="y":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.yellow))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            if part[0] =="b":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.blue))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            if part[0] =="w":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.white))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            if part[0] =="m":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.magenta))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            if part[0] =="c":
                formatContentPart.setForeground(QColor(Qt.GlobalColor.cyan))
                cursor.insertText(part[1:], formatContentPart)
                cursor.insertText(' ', formatContent)
                continue
            cursor.insertText(part, formatContent)
            cursor.insertText(' ', formatContent)
        cursor.endEditBlock()
        self.logTextEdit.append("")

    def scrollToBottom(self):
        # 获取垂直滚动条
        scrollbar = self.logTextEdit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
