# !/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fad

from __future__ import absolute_import, division, print_function, unicode_literals

from Common.ui.cmenutoolbar import FMenuToolBar
from Common.ui.common import FWidget
from configuration import Config
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtWidgets import QToolBar


class MenuToolBar(FMenuToolBar, FWidget):
    def __init__(self, parent=None, *args, **kwargs):
        FMenuToolBar.__init__(self, parent, *args, **kwargs)

        from ui.statistics import StatisticsViewWidget
        from ui.trash_cpt import DebtsTrashViewWidget
        from ui.debt_manager import DebtsViewWidget

        menu = [
            {
                "name": "Statistiques",
                "icon": "state",
                "admin": False,
                "shortcut": "Ctrl+S",
                "goto": StatisticsViewWidget,
            },
            {
                "name": "G. comptes",
                "icon": "compte",
                "admin": False,
                "shortcut": "Ctrl+V",
                "goto": DebtsViewWidget,
            },
            {
                "name": "Poubelle",
                "icon": "del",
                "del": False,
                "shortcut": "Ctrl+P",
                "goto": DebtsTrashViewWidget,
            },
        ]

        for m in menu:
            self.addSeparator()
            self.addAction(
                QIcon("{}{}.png".format(Config.img_media, m.get("icon"))),
                m.get("name"),
                lambda goto=m["goto"]: self.goto(goto),
            )
