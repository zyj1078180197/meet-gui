import os
import sys


def get_path_relative_to_exe(*files):
    """
    获取相对于可执行文件的文件路径。

    此函数用来获取指定文件相对于当前可执行文件的路径。它首先判断当前应用是作为捆绑的可执行文件运行还是作为Python脚本运行，
    然后据此确定应用的基路径，并最终拼接出指定文件的绝对路径。

    参数:
    *files: 可变参数，代表要获取路径的文件名或子目录名。

    返回:
    指定文件相对于当前可执行文件的规范化路径。如果输入的文件名中有None，则返回None。
    """
    # 检查文件参数中是否有None，如果是，则直接返回None
    for file in files:
        if file is None:
            return

    # 判断当前应用是否作为捆绑的可执行文件运行
    if getattr(sys, 'frozen', False):
        # 应用作为捆绑的可执行文件运行时，获取可执行文件的绝对路径
        application_path = os.path.abspath(sys.executable)
    else:
        # 应用作为Python脚本运行时，获取脚本文件的绝对路径
        application_path = os.path.abspath(sys.argv[0])

    # 获取应用路径所在的目录
    the_dir = os.path.dirname(application_path)

    # 将目录与文件路径拼接起来
    path = os.path.join(the_dir, *files)

    # 规范化路径，以确保路径格式正确
    normalized_path = os.path.normpath(path)

    # 返回规范化后的路径
    return normalized_path
