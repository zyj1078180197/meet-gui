from PySide6.QtWidgets import QLabel, QFileDialog
from qfluentwidgets import PushButton, FluentIcon

from meet.gui.widget.input.ConfigLabelAndWidget import ConfigLabelAndWidget


class LabelAndFileSelect(ConfigLabelAndWidget):
    def __init__(self, task, configDesc, config, key: str, theType):
        super().__init__(configDesc, config, key)
        self.task = task
        self.key = key
        self.theType = theType
        self.button = PushButton(FluentIcon.FOLDER, '请选择文件', self)
        self.button.clicked.connect(self.selectFile)
        self.text = QLabel(text="", parent=self)
        self.updateValue()
        self.addWidget(self.text)
        self.addWidget(self.button)

    def updateValue(self):
        self.text.setText(self.config.get(self.key))

    def valueChanged(self, value):
        self.updateConfig(self.task, value)

    def selectFile(self):
        filePath = QFileDialog.getOpenFileName(self, '请选择文件', self.config.get(self.key), self.theType['filter'])
        if filePath and filePath[0] != '':
            self.text.setText(filePath[0])
            self.valueChanged(filePath[0])
