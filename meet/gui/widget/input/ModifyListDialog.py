from PySide6.QtCore import Signal
from qfluentwidgets import MessageBoxBase, SubtitleLabel, ListWidget, PushButton, FluentIcon, LineEdit


class ModifyListDialog(MessageBoxBase):
    listModified = Signal(list)

    def __init__(self, items, parent):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel("修改", self)
        self.viewLayout.addWidget(self.titleLabel)
        self.originalItems = items
        self.listWidget = ListWidget()
        self.listWidget.addItems(self.originalItems)

        self.moveUpButton = PushButton(FluentIcon.UP, "向上移动")
        self.moveUpButton.clicked.connect(self.moveUp)

        self.moveDownButton = PushButton(FluentIcon.DOWN, "向下移动")
        self.moveDownButton.clicked.connect(self.moveDown)

        self.addButton = PushButton(FluentIcon.ADD, "添加")
        self.addButton.clicked.connect(self.addItem)

        self.removeButton = PushButton(FluentIcon.REMOVE, "移除")
        self.removeButton.clicked.connect(self.removeItem)

        self.yesButton.clicked.connect(self.confirm)

        self.cancelButton.clicked.connect(self.cancel)

        self.viewLayout.addWidget(self.listWidget)
        self.viewLayout.addWidget(self.moveUpButton)
        self.viewLayout.addWidget(self.moveDownButton)
        self.viewLayout.addWidget(self.addButton)
        self.viewLayout.addWidget(self.removeButton)
        self.yesButton.setText("确认")
        self.cancelButton.setText("取消")

    def moveUp(self):
        currentRow = self.listWidget.currentRow()
        if currentRow >= 1:
            item = self.listWidget.takeItem(currentRow)
            self.listWidget.insertItem(currentRow - 1, item)
            self.listWidget.setCurrentRow(currentRow - 1)

    def moveDown(self):
        currentRow = self.listWidget.currentRow()
        if currentRow < self.listWidget.count() - 1:
            item = self.listWidget.takeItem(currentRow)
            self.listWidget.insertItem(currentRow + 1, item)
            self.listWidget.setCurrentRow(currentRow + 1)

    def addItem(self):
        w = AddTextMessageBox(self.window())
        if w.exec():
            self.listWidget.addItem(w.addTextEdit.text())

    def removeItem(self):
        currentRow = self.listWidget.currentRow()
        if currentRow >= 0:
            self.listWidget.takeItem(currentRow)

    def confirm(self):
        itemsText = [self.listWidget.item(i).text() for i in range(self.listWidget.count())]
        self.listModified.emit(itemsText)
        self.close()

    def cancel(self):
        self.listModified.emit(self.originalItems)
        self.close()


class AddTextMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel('添加', self)
        self.addTextEdit = LineEdit(self)

        self.addTextEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.addTextEdit)

        # change the text of button
        self.yesButton.setText('确认')
        self.cancelButton.setText('取消')

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)
        self.addTextEdit.textChanged.connect(self._validateText)

    def _validateText(self, text):
        self.yesButton.setEnabled(True if text is not None and text.strip() else False)
