from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from qfluentwidgets import ScrollArea


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
        self.vBoxLayout.setSpacing(10)
        # 设置布局对齐方式为顶部对齐
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        # 设置布局内容边距
        self.vBoxLayout.setContentsMargins(20, 20, 20, 20)
        self.view.setObjectName('view')
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")

        # 必须给内部的视图也加上透明背景样式
        self.view.setStyleSheet("QWidget{background: transparent}")
        # 设置当前类对象的名称为类名
        self.setObjectName(self.__class__.__name__)

    def addWidget(self, widget, stretch=0, align=Qt.AlignmentFlag.AlignTop):
        self.vBoxLayout.addWidget(widget, stretch, align)
        return widget

    def addLayout(self, layout, stretch=0):
        self.vBoxLayout.addLayout(layout, stretch)
        return layout
