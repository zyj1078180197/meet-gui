from meet.gui.widget.input.LabelAndDoubleSpinBox import LabelAndDoubleSpinBox
from meet.gui.widget.input.LabelAndDropDown import LabelAndDropDown
from meet.gui.widget.input.LabelAndFile import LabelAndFile
from meet.gui.widget.input.LabelAndFolder import LabelAndFolder
from meet.gui.widget.input.LabelAndLineEdit import LabelAndLineEdit
from meet.gui.widget.input.LabelAndSpinBox import LabelAndSpinBox
from meet.gui.widget.input.LabelAndSwitchButton import LabelAndSwitchButton
from meet.gui.widget.input.ModifyListItem import ModifyListItem


def configWidget(task, configType, configDesc, config, key, value):
    theType = configType.get(key) if configType is not None else None
    if theType:
        if theType['type'] == 'dropDown':
            return LabelAndDropDown(task, configDesc, theType['options'], config, key)
        if theType['type'] == 'fileSelect':
            return LabelAndFile(task, configDesc, config, key, theType)
        if theType['type'] == 'folderSelect':
            return LabelAndFolder(task, configDesc, config, key)
    if isinstance(value, bool):
        return LabelAndSwitchButton(task, configDesc, config, key)
    elif isinstance(value, list):
        return ModifyListItem(task, configDesc, config, key)
    elif isinstance(value, int):
        return LabelAndSpinBox(task, configDesc, config, key)
    elif isinstance(value, float):
        return LabelAndDoubleSpinBox(task, configDesc, config, key)
    elif isinstance(value, str):
        return LabelAndLineEdit(task, configDesc, config, key)
    else:
        raise ValueError(f"invalid type {type(value)}, value {value}")
