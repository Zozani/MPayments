#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad
from __future__ import absolute_import, division, print_function, unicode_literals

from Common.models import Settings
from Common.ui.common import FMainWindow
from configuration import Config
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from ui.debt_manager import DebtsViewWidget
from ui.menubar import MenuBar
from ui.menutoolbar import MenuToolBar


class MainWindow(FMainWindow):
    def __init__(self):
        FMainWindow.__init__(self)

        self.setWindowIcon(QIcon.fromTheme("logo", QIcon("{}".format(Config.APP_LOGO))))
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)
        sttg = Settings().get(id=1)
        if sttg.toolbar:
            self.toolbar = MenuToolBar(self)
            ptn = {
                sttg.LEFT: Qt.LeftToolBarArea,
                sttg.RITGH: Qt.RightToolBarArea,
                sttg.TOP: Qt.TopToolBarArea,
                sttg.BOTTOM: Qt.BottomToolBarArea,
            }
            self.addToolBar(ptn.get(sttg.toolbar_position), self.toolbar)

        self.page = DebtsViewWidget

        self.change_context(self.page)

    def page_width(self):
        return self.width() - 100

    def exit(self):
        self.logout()
        self.close()
