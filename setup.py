from setuptools import setup, find_packages

setup(
    name='meet-gui',  # 替换为你的包名
    version='1.0.0',  # 你的包的版本号
    packages=find_packages(),  # 自动找到所有的子包
    install_requires=[
        'darkdetect == 0.8.0',
        'PySide6 == 6.7.2',
        'PySide6 - Fluent - Widgets == 1.6.0',
        'PySide6_Addons == 6.7.2',
        'PySide6_Essentials == 6.7.2',
        'PySideSix - Frameless - Window == 0.3.12',
        'pywin32 == 306',
        'shiboken6 == 6.7.2',
    ],
    author='meet',  # 你的名字
    url='https://github.com/zyj1078180197/meet-gui',  # 你的GitHub仓库URL
    license='GPLv3',  # 指定GPLv3许可证
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',  # 指定Python版本要求
)
