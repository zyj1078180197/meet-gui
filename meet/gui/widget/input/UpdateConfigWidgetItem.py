class UpdateConfigWidgetItem:
    def __init__(self, config, key, value):
        self.key = key
        self.config = config
        self.value = value

    def setValue(self, value):
        self.config[self.key] = value
        self.value = value


def valueToString(obj):
    if isinstance(obj, list):
        return ', '.join(map(str, obj))
    else:
        return str(obj)
