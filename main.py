#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga


import os
import sys

from Common.cmain import cmain
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

if __name__ == "__main__":
    if cmain():
        sys.exit(app.exec_())
