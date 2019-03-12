#!/usr/bin/enc python
# -*- coding: UTF-8 -*-

# @File: main.py
# @Time: 2019-3-8 13:49

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from maingui.compressGUI import CompressFiles

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = CompressFiles()
    MainWindow.show()

sys.exit(app.exec_())