#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: fad

from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from PyQt4.QtGui import (QMessageBox, QIcon, QAction, QPixmap)
from PyQt4.QtCore import SIGNAL

from configuration import Config
from Common.exports import export_database_as_file
from Common.ui.common import FWidget
from Common.ui.cmenubar import FMenuBar
from ui.statistics import StatisticsViewWidget
from ui.debt_manager import DebtsViewWidget


class MenuBar(FMenuBar, FWidget):

    def __init__(self, parent=None, admin=False, *args, **kwargs):
        FMenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.setWindowIcon(QIcon(QPixmap("{}".format(Config.APP_LOGO))))
        self.parent = parent

        menu = [{"name": u"Versements", "icon": 'logo', "admin":
                 False, "shortcut": "Ctrl+V", "goto": DebtsViewWidget},
                {"name": u"Statistiques", "icon": 'state', "admin":
                 False, "shortcut": "Ctrl+S", "goto": StatisticsViewWidget},

                ]

        # Menu aller à
        goto_ = self.addMenu(u"&Aller a")

        for m in menu:
            el_menu = QAction(
                QIcon("{}{}.png".format(Config.img_media, m.get('icon'))), m.get('name'), self)
            el_menu.setShortcut(m.get("shortcut"))
            self.connect(
                el_menu, SIGNAL("triggered()"), lambda m=m: self.goto(m.get('goto')))
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
        help_ = self.addMenu(u"Aide")
        help_.addAction(QIcon("{}help.png".format(Config.img_cmedia)),
                        "Aide", self.goto_help)
        help_.addAction(QIcon("{}info.png".format(Config.img_cmedia)),
                        u"À propos", self.goto_about)

    def goto(self, goto):
        self.change_main_context(goto)

    # Aide
    def goto_help(self):
        pass
        # from ui.help import HTMLEditor
        # self.open_dialog(HTMLEditor, modal=True)
