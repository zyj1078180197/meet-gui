from qfluentwidgets import LineEdit

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndLineEdit(ConfigLabelAndWidget):

    def __init__(self, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.key = key
        self.lineEdit = LineEdit()
        self.updateValue()
        self.lineEdit.textChanged.connect(self.valueChanged)
        self.addWidget(self.lineEdit)

    def updateValue(self):
        self.lineEdit.setText(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(value)
