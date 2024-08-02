from PySide6.QtCore import Qt
from qfluentwidgets import ExpandSettingCard, FluentIcon, PushButton

from meet.gui.widget.input.ConfigItemFactory import configWidget


class ConfigCard(ExpandSettingCard):
    def __init__(self):
        super().__init__(FluentIcon.INFO, 'title', 'description')
        self.reset_config = PushButton(FluentIcon.CANCEL, "重置", self)
        self.addWidget(self.reset_config)
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(10, 0, 10, 0)
        self.config = {'姓名': 11.23}
        self.config_desc = {}

        self.viewLayout.addWidget(configWidget({}, self.config_desc, self.config, "姓名", 11.23))
        self._adjustViewSize()
