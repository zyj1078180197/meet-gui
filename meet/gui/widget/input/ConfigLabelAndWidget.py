from meet.gui.widget.input.LabelAndWidget import LabelAndWidget


class ConfigLabelAndWidget(LabelAndWidget):
    """
    该类继承自LabelAndWidget，用于配置项的显示和管理。

    它的主要作用是根据配置描述初始化控件，并提供方法更新配置值。
    """

    def __init__(self, configDesc, config, key: str):
        """
        初始化方法。

        参数:
        - config_desc: 配置描述字典，用于获取配置项的详细信息。
        - config: 配置字典，用于存储配置项的当前值。
        - key: 配置项的键名。

        该方法首先尝试从配置描述中获取当前配置项的描述信息，如果获取不到，则使用默认值。
        然后调用父类的初始化方法，设置配置项的键名和描述信息。
        """
        desc = None
        self.key = key
        self.config = config
        if configDesc is not None:
            desc = configDesc.get(key)
        super().__init__(key, desc)

    def updateConfig(self, value):
        """
        更新配置方法。

        参数:
        - value: 新的配置项值。

        该方法用于更新配置字典中对应配置项的值。
        """
        self.config[self.key] = value
