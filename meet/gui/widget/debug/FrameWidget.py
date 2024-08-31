import win32api
from PySide6.QtCore import QPoint, QTimer
from PySide6.QtGui import QPainter, QColor, QPen, QFont, QGuiApplication
from PySide6.QtWidgets import QWidget


class FrameWidget(QWidget):
    def __init__(self):
        super(FrameWidget, self).__init__()
        # 初始化鼠标位置为 (0, 0)
        self.layout = None
        self._mousePosition = QPoint(0, 0)
        # 设置部件跟踪鼠标移动
        self.setMouseTracking(True)
        # 创建定时器
        self.timer = QTimer(self)
        # 连接定时器超时信号到更新鼠标位置槽函数
        self.timer.timeout.connect(self.updateMousePosition)
        # 启动定时器，每秒更新一次
        self.timer.start(1000)  # 更新间隔为 1 秒
        # 设置字体大小
        self.mouseFont = QFont()
        self.mouseFont.setPointSize(10)  # 调整字体大小
        # 获取主屏幕的设备像素比
        screen = QGuiApplication.primaryScreen()
        self.scaling = screen.devicePixelRatio()

    def updateMousePosition(self):
        try:
            # 如果部件不可见，则不更新
            if not self.isVisible():
                return
            # 获取鼠标当前位置
            x, y = win32api.GetCursorPos()
            # 将全局坐标转换为相对于本部件的坐标
            relative = self.mapFromGlobal(QPoint(x / self.scaling, y / self.scaling))
            # 如果鼠标位置有变化，则更新
            if self._mousePosition != relative and relative.x() > 0 and relative.y() > 0:
                self._mousePosition = relative
            # 触发重绘事件
            self.update()
        except Exception as e:
            # 打印异常信息
            print(f'GetCursorPos exception {e}')

    def paintEvent(self, event):
        # 如果部件不可见，则不绘制
        if not self.isVisible():
            return
        # 创建画家对象
        painter = QPainter(self)
        # 绘制边框
        self.paintBorder(painter)
        # 绘制鼠标位置信息
        self.paintMousePosition(painter)

    def paintBorder(self, painter):
        # 设置画笔颜色为红色
        pen = QPen(QColor(255, 0, 0, 255))  # 红色画笔
        # 设置画笔宽度
        pen.setWidth(1)
        # 设置画家使用的画笔
        painter.setPen(pen)
        # 绘制边框
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)

    def paintMousePosition(self, painter):
        # 计算鼠标位置相对于部件的百分比
        x_percent = self._mousePosition.x() / self.width()
        y_percent = self._mousePosition.y() / self.height()
        x, y = self._mousePosition.x(), self._mousePosition.y()
        # 构造显示文本
        text = f"({x}, {y}, {x_percent:.2f}, {y_percent:.2f})"
        # 设置字体
        painter.setFont(self.mouseFont)

        # 设置画笔颜色为红色
        painter.setPen(QPen(QColor(255, 0, 0, 255), 1))
        # 在指定位置绘制文本
        painter.drawText(20, 20, text)
