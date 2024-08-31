from datetime import datetime

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QTextCharFormat, QColor, QIcon
from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy

from meet.gui.plugin.Communicate import communicate

log_levels = {
    'INF': Qt.GlobalColor.green,
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
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        # 隐藏滚动条
        self.log_text_edit.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置透明背景
        self.log_text_edit.setStyleSheet("background-color: rgba(0, 0, 0, 25);")
        layout.addWidget(self.log_text_edit)
        self.setGeometry(20, 780, 400, 300)
        communicate.logMsg.connect(self.addLog)

    @Slot()
    def addLog(self, level, message):
        # 日志级别和对应的颜色
        color_level = log_levels.get(level, Qt.GlobalColor.black)
        color_time = Qt.GlobalColor.darkGray
        color_content = Qt.GlobalColor.gray

        # 在文本编辑区中添加日志
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] [{level}] {message}"
        self.insertColoredText(log_message, color_level, color_time, color_content)

        # 文本超过1000行时
        if self.log_text_edit.document().lineCount() > 1000:
            self.log_text_edit.clear()

        # 确保滚动条在最新消息的位置
        self.scrollToBottom()

    def insertColoredText(self, text, color_level, color_time, color_content):
        cursor = self.log_text_edit.textCursor()
        format_level = QTextCharFormat()
        format_level.setForeground(QColor(color_level))

        format_time = QTextCharFormat()
        format_time.setForeground(QColor(color_time))

        format_content = QTextCharFormat()
        format_content.setForeground(QColor(color_content))

        parts = text.split()
        cursor.beginEditBlock()
        cursor.insertText(parts[0], format_time)  # 日志级别
        cursor.insertText('  ', format_content)
        cursor.insertText(parts[1], format_level)  # 时间戳
        cursor.insertText('  ', format_content)
        for part in parts[2:].__str__().split("#"):
            if part == "[\'" or part == "\']":
                continue
            formatContent = QTextCharFormat()
            #第一个字符判断
            if part[0] =="r":
                formatContent.setForeground(QColor(Qt.GlobalColor.red))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            if part[0] =="g":
                formatContent.setForeground(QColor(Qt.GlobalColor.green))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            if part[0] =="y":
                formatContent.setForeground(QColor(Qt.GlobalColor.yellow))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            if part[0] =="b":
                formatContent.setForeground(QColor(Qt.GlobalColor.blue))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            if part[0] =="w":
                formatContent.setForeground(QColor(Qt.GlobalColor.white))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            if part[0] =="m":
                formatContent.setForeground(QColor(Qt.GlobalColor.magenta))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            if part[0] =="c":
                formatContent.setForeground(QColor(Qt.GlobalColor.cyan))
                cursor.insertText(part[1:], formatContent)
                cursor.insertText(' ', format_content)
                continue
            cursor.insertText(part, format_content)
            cursor.insertText(' ', format_content)
        cursor.endEditBlock()
        self.log_text_edit.append("")

    def scrollToBottom(self):
        # 获取垂直滚动条
        scrollbar = self.log_text_edit.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
