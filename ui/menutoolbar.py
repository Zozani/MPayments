# !/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fad

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QIcon, QToolBar, QFont, QCursor)
from PyQt4.QtCore import Qt, QSize

from Common.ui.common import FWidget

from configuration import Config

# from ui.dashboard import DashbordViewWidget
from ui.payment import PaymentViewWidget
from ui.debt_manager import DebtsViewWidget


class MenuToolBar(QToolBar, FWidget):

    def __init__(self, parent=None, *args, **kwargs):
        QToolBar.__init__(self, parent, *args, **kwargs)

        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QSize(35, 35))
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(35)
        self.setFont(font)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setFocusPolicy(Qt.TabFocus)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.setAcceptDrops(True)
        # self.setAutoFillBackground(True)

        self.addSeparator()
        self.addAction(
            QIcon(u"{}exit.png".format(Config.img_cmedia)), u"Quiter", self.goto_exit)
        menu = [{"name": u"Versement", "admin": True,
                 "icon": 'logo', "goto": PaymentViewWidget},
                {"name": u"Dettes", "admin": True,
                 "icon": 'debt', "goto": DebtsViewWidget},
                ]

        for m in menu:
            self.addSeparator()
            self.addAction(QIcon("{}{}.png".format(Config.img_media, m.get('icon'))),
                           m.get('name'), lambda m=m: self.goto(m.get('goto')))

    def goto(self, goto):
        self.change_main_context(goto)

    def goto_exit(self):
        self.parent().exit()
