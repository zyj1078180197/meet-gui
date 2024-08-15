from PySide6.QtWidgets import QLabel
from qfluentwidgets import PushButton

from meet.gui.widget.input.UpdateConfigWidgetItem import valueToString
from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget
from meet.gui.widget.input.ModifyListDialog import ModifyListDialog


class ModifyListItem(ConfigLabelAndWidget):

    def __init__(self, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.switchButton = PushButton("修改", parent=self)
        self.switchButton.setFixedWidth(100)
        self.switchButton.clicked.connect(self.clicked)
        self.listText = QLabel("")
        self.updateValue()
        self.addWidget(self.listText)
        self.addWidget(self.switchButton)

    def updateValue(self):
        items = self.config.get(self.key)
        totalLength = sum(len(item) for item in items)

        if totalLength > 30:
            displayText = "\n".join(items)
        else:
            displayText = valueToString(items)

        self.listText.setText(displayText)

    def clicked(self):
        dialog = ModifyListDialog(self.config.get(self.key), self.window())
        dialog.listModified.connect(self.listModified)
        dialog.exec()

    def listModified(self, theList):
        self.updateConfig(theList)
        self.updateValue()
