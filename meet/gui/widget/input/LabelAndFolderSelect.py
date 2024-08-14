from PySide6.QtWidgets import QLabel, QFileDialog
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndFolderSelect(ConfigLabelAndWidget):
    def __init__(self, task, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.task = task
        self.key = key
        self.button = PushButton(FluentIcon.FOLDER, '请选择文件夹', self)
        self.button.clicked.connect(self.selectFolder)
        self.text = QLabel(text="", parent=self)
        self.updateValue()
        self.addWidget(self.text)
        self.addWidget(self.button)

    def updateValue(self):
        self.text.setText(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(self.task, value)

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, '请选择文件夹', self.config.get(self.key))
        if folderPath:
            self.text.setText(folderPath)
            self.valueChanged(folderPath)
