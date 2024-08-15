from meet.gui.widget.input.LabelAndDoubleSpinBox import LabelAndDoubleSpinBox
from meet.gui.widget.input.LabelAndDropDown import LabelAndDropDown
from meet.gui.widget.input.LabelAndFileSelect import LabelAndFileSelect
from meet.gui.widget.input.LabelAndFolderSelect import LabelAndFolderSelect
from meet.gui.widget.input.LabelAndLineEdit import LabelAndLineEdit
from meet.gui.widget.input.LabelAndSpinBox import LabelAndSpinBox
from meet.gui.widget.input.LabelAndSwitchButton import LabelAndSwitchButton
from meet.gui.widget.input.ModifyListItem import ModifyListItem


def configWidget(configType, configDesc, config, key, value):
    theType = configType.get(key) if configType is not None else None
    if theType:
        if theType['type'] == 'dropDown':
            return LabelAndDropDown(configDesc, theType['options'], config, key)
        if theType['type'] == 'fileSelect':
            return LabelAndFileSelect(configDesc, config, key, theType)
        if theType['type'] == 'folderSelect':
            return LabelAndFolderSelect(configDesc, config, key)
    if isinstance(value, bool):
        return LabelAndSwitchButton(configDesc, config, key)
    elif isinstance(value, list):
        return ModifyListItem(configDesc, config, key)
    elif isinstance(value, int):
        return LabelAndSpinBox(configDesc, config, key)
    elif isinstance(value, float):
        return LabelAndDoubleSpinBox(configDesc, config, key)
    elif isinstance(value, str):
        return LabelAndLineEdit(configDesc, config, key)
    else:
        raise ValueError(f"invalid type {type(value)}, value {value}")
