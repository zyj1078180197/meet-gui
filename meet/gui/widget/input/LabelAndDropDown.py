from qfluentwidgets import ComboBox

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndDropDown(ConfigLabelAndWidget):

    def __init__(self, configDesc, options, config, key: str):
        super().__init__(configDesc, config, key)
        self.key = key
        self.dict = {}
        self.options = []
        for option in options:
            self.options.append(option)
            self.dict[option] = option
        self.comboBox = ComboBox()
        self.comboBox.addItems(self.options)
        self.comboBox.setCurrentIndex(findStringIndex(options, self.config.get(self.key)))
        self.comboBox.setMinimumWidth(210)
        self.comboBox.currentTextChanged.connect(self.textChanged)
        self.addWidget(self.comboBox)

    def textChanged(self, text):
        option = self.dict.get(text)
        self.updateConfig(option)

    def updateValue(self):
        self.comboBox.setText(self.config.get(self.key))


def findStringIndex(myList, targetString):
    try:
        index = myList.index(targetString)
        return index
    except ValueError:
        return 0
