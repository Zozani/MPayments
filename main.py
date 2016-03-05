#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
import sys
import locale
import gettext

sys.path.append(os.path.abspath('../'))

from Common import gettext_windows

from PyQt4.QtGui import QApplication

from database import setup
from Common.ui.window import FWindow
from Common.cmain import cmain
from Common.ui.qss import appStyle

from ui.mainwindow import MainWindow

app = QApplication(sys.argv)


def main():
    """  """
    gettext_windows.setup_env()
    locale.setlocale(locale.LC_ALL, '')
    # gettext.install('bmain', localedir='locale', unicode=True)
    gettext.install('main.py', localedir='locale')
    window = MainWindow()
    window.setStyleSheet(appStyle)
    setattr(FWindow, 'window', window)
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    setup()
    # main()
    if cmain():
        main()
