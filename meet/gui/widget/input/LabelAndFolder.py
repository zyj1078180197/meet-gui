from PySide6.QtWidgets import QLabel, QFileDialog
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndFolder(ConfigLabelAndWidget):
    def __init__(self, task, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.task = task
        self.key = key
        self.button = PushButton(FluentIcon.FOLDER, '请选择文件夹', self)
        self.button.clicked.connect(self.selectFolder)
        self.listText = QLabel(text="", parent=self)
        self.updateValue()
        self.addWidget(self.listText)
        self.addWidget(self.button)

    def updateValue(self):
        self.listText.setText(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(self.task, value)

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, '请选择文件夹', self.config.get(self.key))
        if folderPath:
            self.listText.setText(folderPath)
            self.valueChanged(folderPath)
