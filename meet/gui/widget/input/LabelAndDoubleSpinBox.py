from qfluentwidgets import DoubleSpinBox

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndDoubleSpinBox(ConfigLabelAndWidget):

    def __init__(self, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.key = key
        self.spinBox = DoubleSpinBox()
        self.spinBox.setFixedWidth(300)
        self.updateValue()
        self.spinBox.valueChanged.connect(self.valueChanged)
        self.addWidget(self.spinBox)

    def updateValue(self):
        self.spinBox.setValue(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(value)
