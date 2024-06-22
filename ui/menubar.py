#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fad

from __future__ import absolute_import, division, print_function, unicode_literals

from Common.ui.cmenubar import FMenuBar
from Common.ui.common import FWidget
from configuration import Config
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAction

# from PyQt5.QtCore import SIGNAL


class MenuBar(FMenuBar, FWidget):
    def __init__(self, parent=None, admin=False, *args, **kwargs):
        FMenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.setWindowIcon(QIcon(QPixmap("{}".format(Config.APP_LOGO))))
        self.parent = parent

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

        # Menu aller à
        goto_ = self.addMenu("&Aller a")

        for m in menu:
            el_menu = QAction(
                QIcon(f"{Config.img_media}{m.get('icon')}.png"),
                m.get("name"),
                self,
            )
            el_menu.setShortcut(m.get("shortcut"))
            el_menu.triggered.connect(lambda checked, m=m: self.goto(m.get("goto")))
            goto_.addSeparator()
            goto_.addAction(el_menu)

        # if admin:
        # all report
        #     all_report = QAction(u"Tous les rapports", self)
        #     all_report.setShortcut("Ctrl+T")
        #     self.connect(all_report, SIGNAL("triggered()"),
        #                                         self.all_report)
        #     goto_.addAction(all_report)

        # Menu Aide
        help_ = self.addMenu("Aide")
        help_.addAction(
            QIcon("{}help.png".format(Config.img_cmedia)), "Aide", self.goto_help
        )
        help_.addAction(
            QIcon("{}info.png".format(Config.img_cmedia)), "À propos", self.goto_about
        )

    def goto(self, goto):
        self.change_main_context(goto)

    # Aide
    def goto_help(self):
        pass
        # from ui.help import HTMLEditor
        # self.open_dialog(HTMLEditor, modal=True)
