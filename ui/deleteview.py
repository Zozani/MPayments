#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from __future__ import absolute_import, division, print_function, unicode_literals

from Common.ui.common import Button, FLabel, FPageTitle, FWidget
from PyQt5.QtWidgets import QDialog, QGridLayout, QHBoxLayout, QVBoxLayout


class DeleteViewWidget(QDialog, FWidget):
    def __init__(self, table_p, obj, parent, *args, **kwargs):
        super(DeleteViewWidget, self).__init__(parent, *args, **kwargs)

        self.setWindowTitle("Confirmation de suppression")

        # Set the title using the object's provider name
        self.title = FPageTitle("<h2>Compte : {}</h2>".format(obj.provider_clt.name))
        self.obj = obj
        self.table_p = table_p
        # Use getattr to avoid AttributeError if provid_clt_id does not exist
        self.provid_clt_id = getattr(table_p, "provid_clt_id", None)
        self.parent = parent

        # Create the title layout
        title_hbox = QHBoxLayout()
        title_hbox.addWidget(self.title)

        # Create the report layout
        report_hbox = QGridLayout()
        report_hbox.addWidget(FLabel(obj.display_name()), 0, 0)

        # Create the button layout
        button_box = QHBoxLayout()

        # Create and configure the delete button
        delete_but = Button("Supprimer")
        button_box.addWidget(delete_but)
        delete_but.clicked.connect(self.delete)

        # Create and configure the cancel button
        cancel_but = Button("Annuler")
        button_box.addWidget(cancel_but)
        cancel_but.clicked.connect(self.cancel)

        # Create the main layout
        vbox = QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(report_hbox)
        vbox.addLayout(button_box)
        self.setLayout(vbox)

    def cancel(self):
        """Close the dialog and return False."""
        self.close()
        return False

    def delete(self):
        """Delete the object, refresh the parent table, and notify the parent."""
        self.obj.deletes_data()
        self.cancel()
        if self.provid_clt_id is not None:
            self.table_p.refresh_(provid_clt_id=self.provid_clt_id)
        self.parent.Notify("Le rapport a été bien supprimé", "error")
