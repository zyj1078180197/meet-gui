from enum import Enum

from meet.gui.widget.trigger.TriggerCard import TriggerCard, TriggerExpandCard
from meet.gui.widget.trigger.TriggerTab import TriggerTab
from meet.executor.trigger.TriggerExecutor import TriggerExecutor
from meet.util.Class import getClassByName


class RealTimeTriggerTab(TriggerTab):
    class ShowStyle(Enum):
        NORMAL = 'Normal'
        EXPAND = 'Expand'
    # 任务类集合
    baseTriggerList=[]
    def __init__(self, parent=None):
        super().__init__(parent)
        for triggerList in TriggerExecutor.triggerList:
            for trigger in triggerList:
                baseTrigger = TriggerExecutor.baseTriggerDict.get(trigger.get("triggerId"))
                RealTimeTriggerTab.baseTriggerList.append(baseTrigger)
                if trigger.get("showStyle") == RealTimeTriggerTab.ShowStyle.EXPAND.value:
                    triggerExpandCard = TriggerExpandCard(trigger, baseTrigger, self)
                    self.addWidget(triggerExpandCard)
                else:
                    triggerCard = TriggerCard(trigger, baseTrigger, self)
                    self.addWidget(triggerCard)
        self.setObjectName("触发")

    def closeEvent(self, event):
        self.deleteLater()
        event.accept()