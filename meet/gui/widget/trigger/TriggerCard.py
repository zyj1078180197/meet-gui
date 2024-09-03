from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import SwitchButton

from meet.executor.trigger.BaseTrigger import BaseTrigger
from meet.executor.trigger.TriggerExecutor import TriggerExecutor
from meet.gui.widget.trigger.ConfigCard import ConfigCard, ConfigExpandCard
from meet.util.MessageTips import showSuccess


class TriggerCard(ConfigCard):
    def __init__(self, trigger, baseTrigger, parent=None):
        super().__init__(trigger, parent=parent)
        self.parentTab = parent
        triggerButton = TriggerButtons(self, trigger, baseTrigger)
        self.clicked.connect(lambda: TriggerButtons.editClicked(trigger, baseTrigger))
        self.addWidget(triggerButton)


class TriggerExpandCard(ConfigExpandCard):
    def __init__(self, trigger, baseTrigger, parent=None):
        super().__init__(trigger, baseTrigger, parent=parent)
        self.parentTab = parent
        triggerButton = TriggerButtons(self, trigger, baseTrigger)
        self.addWidget(triggerButton)


class TriggerButtons(QWidget):
    def __init__(self, parent: TriggerCard | TriggerExpandCard, trigger, baseTrigger):
        self.stopEvent = None
        self.trigger = trigger
        self.menu = None
        self.baseTrigger = baseTrigger
        super().__init__(parent=parent)
        self.parent: TriggerCard | TriggerExpandCard = parent
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(18)
        button = SwitchButton()
        from meet.executor.trigger.BaseTrigger import BaseTrigger
        if baseTrigger.status == BaseTrigger.StatusEnum.RUNNING.value:
            button.setChecked(True)
        else:
            button.setChecked(False)
        button.setOffText("关")
        button.setOnText("开")
        button.checkedChanged.connect(self.checkedChange)

        self.layout.addWidget(button)

    def checkedChange(self, checked):
        if checked:
            self.startClicked(self.baseTrigger)
            self.trigger['status'] = BaseTrigger.StatusEnum.RUNNING.value
            self.parent.saveConfigValue()
        else:
            self.stopClicked(self.baseTrigger)
            self.trigger['status'] = BaseTrigger.StatusEnum.STOPPED.value
            self.parent.saveConfigValue()

    @staticmethod
    def startClicked(baseTrigger):
        from meet.executor.trigger.BaseTrigger import BaseTrigger
        baseTrigger.status = BaseTrigger.StatusEnum.RUNNING.value
        baseTrigger.job = TriggerExecutor.addJob(baseTrigger)
        showSuccess(baseTrigger.title + "启动")

    @staticmethod
    def stopClicked(baseTrigger):
        from meet.executor.trigger.BaseTrigger import BaseTrigger
        baseTrigger.status = BaseTrigger.StatusEnum.STOPPED.value
        baseTrigger.job.remove()
        showSuccess(baseTrigger.title + "关闭")

    @staticmethod
    def editClicked(trigger, baseTrigger):
        from meet.config.GlobalGui import globalGui
        from meet.gui.widget.trigger.TriggerEditTab import TriggerEditTab
        # 添加新的页面，用于处理配置的改变
        page = globalGui.meet.window.editPageDict.get("编辑触发:" + str(trigger.get("triggerId")))
        if page is None:
            page = TriggerEditTab(trigger, baseTrigger)
            page.setObjectName("编辑触发:" + str(trigger.get("triggerId")))
        globalGui.meet.openEditPage(page, "编辑触发:" + str(trigger.get("triggerId")))
