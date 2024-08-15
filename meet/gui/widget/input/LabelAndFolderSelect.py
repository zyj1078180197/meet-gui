from PySide6.QtWidgets import QFileDialog
from qfluentwidgets import PushButton, FluentIcon, CaptionLabel

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndFolderSelect(ConfigLabelAndWidget):
    def __init__(self, configDesc, config, key: str):
        super().__init__(configDesc, config, key)
        self.key = key
        self.button = PushButton(FluentIcon.FOLDER, '请选择文件夹', self)
        self.button.clicked.connect(self.selectFolder)
        self.text = CaptionLabel(text="", parent=self)
        self.updateValue()
        self.addWidget(self.text)
        self.addWidget(self.button)

    def updateValue(self):
        self.text.setText(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(value)

    def selectFolder(self):
        folderPath = QFileDialog.getExistingDirectory(self, '请选择文件夹', self.config.get(self.key))
        if folderPath:
            self.text.setText(folderPath)
            self.valueChanged(folderPath)
