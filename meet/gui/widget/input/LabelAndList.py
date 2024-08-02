from qfluentwidgets import SpinBox

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndDoubleSpinBox(ConfigLabelAndWidget):

    def __init__(self, config, configDesc, key: str):
        super().__init__(configDesc, config, key)
        self.key = key
        self.config = config
        self.spinBox = SpinBox()
        self.spinBox.setValue(self.config[self.key])
        self.spinBox.valueChanged.connect(self.valueChanged)
        self.addWidget(self.spinBox)

    def valueChanged(self, value):
        self.config[self.key] = value
