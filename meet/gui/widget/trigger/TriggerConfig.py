from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy, QSpacerItem
from qfluentwidgets import BodyLabel, CaptionLabel, ComboBox, LineEdit, DoubleSpinBox

from meet.gui.widget.trigger.ConfigCard import ConfigExpandCard
from meet.gui.widget.trigger.TriggerEditTab import TriggerEditTab


class ConfigMode(QWidget):
    def __init__(self, parent: ConfigExpandCard | TriggerEditTab = None, baseTrigger=None, trigger=None):
        super().__init__(parent)
        self.baseTrigger = baseTrigger
        self.trigger = trigger
        self.parent: ConfigExpandCard | TriggerEditTab = parent
        # 初始化水平布局作为主布局
        self.layout = QHBoxLayout(self)
        # 初始化用于放置标题和内容的垂直布局
        self.titleLayout = QVBoxLayout(self)
        # 将垂直布局添加到主布局中
        self.layout.addLayout(self.titleLayout)
        # 创建并设置标题标签
        self.title = BodyLabel("触发类型", self)
        self.title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # 将标题标签添加到垂直布局中
        self.titleLayout.addWidget(self.title)
        # 如果存在内容参数，则创建并添加内容标签
        self.contentLabel = CaptionLabel("Cron表达式或者Interval间隔时间触发", self)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.contentLabel.setObjectName('contentLabel')
        self.titleLayout.addWidget(self.contentLabel)
        # 添加一个扩展的空格项到主布局，用于调整布局内的空间
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.comboBox = ComboBox(self)
        self.comboBox.setFixedWidth(300)
        self.options = ["Cron", "Interval"]
        self.comboBox.addItems(self.options)
        self.comboBox.setCurrentIndex(self.options.index(baseTrigger.triggerMode))
        self.comboBox.currentTextChanged.connect(self.textChange)
        self.layout.addWidget(self.comboBox)

    def textChange(self, text):
        self.baseTrigger.triggerMode = text
        self.trigger['triggerMode'] = self.baseTrigger.triggerMode
        from meet.executor.trigger.BaseTrigger import BaseTrigger
        if self.baseTrigger.triggerMode == BaseTrigger.TriggerModeEnum.CRON.value:
            self.parent.cronMode()
        if self.baseTrigger.triggerMode == "Interval":
            self.parent.intervalMode()


class ConfigCron(QWidget):
    def __init__(self, parent=None, baseTrigger=None, trigger=None):
        super().__init__(parent)
        self.baseTrigger = baseTrigger
        self.trigger = trigger
        # 初始化水平布局作为主布局
        self.layout = QHBoxLayout(self)
        # 初始化用于放置标题和内容的垂直布局
        self.titleLayout = QVBoxLayout(self)
        # 将垂直布局添加到主布局中
        self.layout.addLayout(self.titleLayout)
        # 创建并设置标题标签
        self.title = BodyLabel("Cron表达式", self)
        self.title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # 将标题标签添加到垂直布局中
        self.titleLayout.addWidget(self.title)
        # 如果存在内容参数，则创建并添加内容标签
        self.contentLabel = CaptionLabel("Cron表达式如：*/1 * * * * *(每一秒触发一次)", self)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.contentLabel.setObjectName('contentLabel')
        self.titleLayout.addWidget(self.contentLabel)
        # 添加一个扩展的空格项到主布局，用于调整布局内的空间
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.lineEdit = LineEdit(self)
        self.lineEdit.setFixedWidth(300)
        self.lineEdit.setText(baseTrigger.cron)
        self.lineEdit.textChanged.connect(self.textChange)
        self.layout.addWidget(self.lineEdit)

    def textChange(self, text):
        self.baseTrigger.cron = text
        self.trigger["cron"] = self.baseTrigger.cron


class ConfigInterval(QWidget):
    def __init__(self, parent=None, baseTrigger=None, trigger=None):
        super().__init__(parent)
        self.baseTrigger = baseTrigger
        self.trigger = trigger
        # 初始化水平布局作为主布局
        self.layout = QHBoxLayout(self)
        # 初始化用于放置标题和内容的垂直布局
        self.titleLayout = QVBoxLayout(self)
        # 将垂直布局添加到主布局中
        self.layout.addLayout(self.titleLayout)
        # 创建并设置标题标签
        self.title = BodyLabel("Interval间隔时间", self)
        self.title.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        # 将标题标签添加到垂直布局中
        self.titleLayout.addWidget(self.title)
        # 如果存在内容参数，则创建并添加内容标签
        self.contentLabel = CaptionLabel("Interval间隔时间如：1(每一秒触发一次)", self)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.contentLabel.setObjectName('contentLabel')
        self.titleLayout.addWidget(self.contentLabel)
        # 添加一个扩展的空格项到主布局，用于调整布局内的空间
        self.layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.doubleEdit = DoubleSpinBox(self)
        self.doubleEdit.setFixedWidth(300)
        self.doubleEdit.setValue(baseTrigger.interval)
        self.doubleEdit.valueChanged.connect(self.valueChange)
        self.layout.addWidget(self.doubleEdit)

    def valueChange(self, text):
        self.baseTrigger.interval = text
        self.trigger["interval"] = self.baseTrigger.interval
