from qfluentwidgets import SwitchButton

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndSwitchButton(ConfigLabelAndWidget):

    def __init__(self, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.key = key
        self.switchButton = SwitchButton()
        self.switchButton.setOnText('是')
        self.switchButton.setOffText('否')
        self.updateValue()
        self.switchButton.checkedChanged.connect(self.checkChanged)
        self.addWidget(self.switchButton)

    def updateValue(self):
        self.switchButton.setChecked(self.config.get(self.key))

    def checkChanged(self, checked):
        self.updateConfig(checked)
