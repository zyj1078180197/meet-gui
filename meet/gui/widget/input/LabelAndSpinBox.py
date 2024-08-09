from qfluentwidgets import SpinBox

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndSpinBox(ConfigLabelAndWidget):

    def __init__(self, task,configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.task = task
        self.key = key
        self.spinBox = SpinBox()
        self.spinBox.setRange(1, 99999999)
        self.spinBox.setFixedWidth(300)
        self.updateValue()
        self.spinBox.valueChanged.connect(self.valueChanged)
        self.addWidget(self.spinBox)

    def updateValue(self):
        self.spinBox.setValue(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(self.task,value)
