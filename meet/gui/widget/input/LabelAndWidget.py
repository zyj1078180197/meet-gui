from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QSizePolicy, QSpacerItem


class LabelAndWidget(QWidget):
    """
    一个继承自QWidget的类，用于创建一个包含标签和小部件的布局。

    该类的目的是简化创建包含标题和内容标签以及可动态添加其他小部件的布局的过程。
    它使用QHBoxLayout作为主布局，内部包含一个QVBoxLayout用于标题和内容标签，以及一个QSpacerItem用于调整布局内的空间。
    """

    def __init__(self, title: str, content=None):
        """
        初始化函数。

        参数:
        title: str - 标题标签的文本。
        content: str, optional - 内容标签的文本，默认为空。

        该函数设置主布局为QHBoxLayout，并在内部创建一个包含标题和可选内容的QVBoxLayout。
        """
        super().__init__()
        # 初始化水平布局作为主布局
        self.layout = QHBoxLayout(self)
        # 初始化用于放置标题和内容的垂直布局
        self.titleLayout = QVBoxLayout()
        # 将垂直布局添加到主布局中
        self.layout.addLayout(self.titleLayout)
        # 创建并设置标题标签
        self.title = QLabel(title)
        self.title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # 将标题标签添加到垂直布局中
        self.titleLayout.addWidget(self.title)
        # 如果存在内容参数，则创建并添加内容标签
        if content:
            self.contentLabel = QLabel(content)
            self.contentLabel.setObjectName('contentLabel')
            self.titleLayout.addWidget(self.contentLabel)
        # 添加一个扩展的空格项到主布局，用于调整布局内的空间
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

    def addWidget(self, widget: QWidget):
        """
        将小部件添加到布局中的函数。

        参数:
        widget: QWidget - 要添加到布局中的小部件。

        该函数将给定的小部件添加到主布局中。
        """
        # 将小部件添加到主布局中
        self.layout.addWidget(widget)
