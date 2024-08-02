from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from qfluentwidgets import ScrollArea

from meet.gui.plugin.Communicate import communicate
from meet.util.Theme import isDarkTheme


class Tab(ScrollArea):
    def __init__(self):
        super().__init__()
        # 创建一个QWidget作为视图，并设置为该类的属性
        self.view = QWidget(self)
        # 创建一个QVBoxLayout，并将视图作为其父对象
        self.vBoxLayout = QVBoxLayout(self.view)

        # 设置水平滚动条策略为永远关闭
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 设置视口边距为0
        self.setViewportMargins(0, 0, 0, 0)
        # 设置视图为当前类的部件
        self.setWidget(self.view)
        # 设置部件是否可以调整大小
        self.setWidgetResizable(True)
        # 设置大小策略为水平方向扩展，垂直方向最小
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # 设置布局间距为30
        self.vBoxLayout.setSpacing(30)
        # 设置布局对齐方式为顶部对齐
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # 设置布局内容边距
        self.vBoxLayout.setContentsMargins(36, 20, 36, 36)
        self.view.setObjectName('view')
        if isDarkTheme():
            self.view.setStyleSheet("background-color: #1A212E;")
        else:
            self.view.setStyleSheet("background-color: #ffffff;")
        # 主题改变事件
        communicate.themeChange.connect(self.themeChange)
        # 设置当前类对象的名称为类名
        self.setObjectName(self.__class__.__name__)

    def addWidget(self, widget, stretch=0, align=Qt.AlignmentFlag.AlignTop):
        self.vBoxLayout.addWidget(widget, stretch, align)
        return widget

    def addLayout(self, layout, stretch=0):
        self.vBoxLayout.addLayout(layout, stretch)
        return layout

    def themeChange(self):
        if isDarkTheme():
            self.view.setStyleSheet("background-color: #1A212E;")
        else:
            self.view.setStyleSheet("background-color: #ffffff;")
