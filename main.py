#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import unicode_literals, absolute_import, division, print_function

import os
import sys

sys.path.append(os.path.abspath('../'))

from PyQt4.QtGui import QApplication

from Common.cmain import cmain


app = QApplication(sys.argv)


def main():

    # window = MainWindow()
    # window.setStyleSheet(theme)
    # setattr(FWindow, 'window', window)
    # # window.show()
    # window.showMaximized()
    # sys.exit(app.exec_())
    print('kdk')


if __name__ == '__main__':
    if cmain():
        sys.exit(app.exec_())
