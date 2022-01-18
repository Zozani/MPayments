#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad

from PyQt5.QtWidgets import QVBoxLayout, QDialog, QTextEdit, QFormLayout, QComboBox

from Common.ui.util import check_is_empty, field_error
from Common.ui.common import FWidget, Button, FormLabel, LineEdit, IntLineEdit
import peewee
from models import ProviderOrClient

from configuration import Config


class EditOrAddClientOrProviderDialog(QDialog, FWidget):
    def __init__(self, table_p, parent, prov_clt=None, *args, **kwargs):
        FWidget.__init__(self, parent, *args, **kwargs)

        self.table_p = table_p
        self.prov_clt = prov_clt
        self.parent = parent
        if self.prov_clt:
            self.new = False
            self.title = u"Modification de {} {}".format(
                self.prov_clt.type_, self.prov_clt.name
            )
            self.succes_msg = u"{} a été bien mise à jour".format(self.prov_clt.type_)
        else:
            self.new = True
            self.succes_msg = u"Client a été bien enregistré"
            self.title = u"Création d'un nouvel client"
            self.prov_clt = ProviderOrClient()
        self.setWindowTitle(self.title)

        vbox = QVBoxLayout()
        # vbox.addWidget(FPageTitle(u"Utilisateur: %s " % self.prov_clt.name))
        self.liste_devise = ProviderOrClient.DEVISE
        # Combobox widget
        self.box_devise = QComboBox()
        for index, value in enumerate(self.liste_devise):
            self.box_devise.addItem("{} {}".format(self.liste_devise[value], value))
            if self.prov_clt.devise == value:
                self.box_devise.setCurrentIndex(index)

        if self.prov_clt.phone:
            phone = str(self.prov_clt.phone)
        else:
            phone = ""
        self.nameField = LineEdit(self.prov_clt.name)
        self.phone_field = IntLineEdit(phone)
        # self.phone_field.setInputMask("D9.99.99.99")
        self.legal_infos = LineEdit(self.prov_clt.legal_infos)
        self.address = QTextEdit(self.prov_clt.address)
        self.email = LineEdit(self.prov_clt.email)

        formbox = QFormLayout()
        formbox.addRow(FormLabel(u"Nom complete : *"), self.nameField)

        if Config.DEVISE_PEP_PROV:
            formbox.addRow(FormLabel(u"Devise :"), self.box_devise)

        if not self.new:
            formbox.addRow(FormLabel(u"Tel: *"), self.phone_field)
            formbox.addRow(FormLabel(u"E-mail :"), self.email)
            formbox.addRow(FormLabel(u"addresse complete :"), self.address)
            formbox.addRow(FormLabel(u"Info. legale :"), self.legal_infos)

        butt = Button(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        formbox.addRow("", butt)

        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def save_edit(self):
        """add operation"""
        # print("Save")
        phone = self.phone_field.text()
        # field_error
        if check_is_empty(self.nameField):
            return

        prov_clt = self.prov_clt
        prov_clt.name = str(self.nameField.text())

        if Config.DEVISE_PEP_PROV:
            prov_clt.devise = str(self.box_devise.currentText().split()[1])

        if not self.new:
            if phone != "":
                prov_clt.phone = int(phone)
            prov_clt.email = str(self.email.text())
            prov_clt.legal_infos = str(self.legal_infos.text())
            prov_clt.address = str(self.address.toPlainText())

        try:
            prov_clt.save()
            self.close()
            self.table_p.refresh_()
            # self.parent.Notify(u"Le Compte %s a été mise à jour" %
            #                    prov_clt.name, "success")
        except peewee.IntegrityError as e:
            # print("IntegrityError ", e)
            field_error(self.nameField, "Ce nom existe dans la basse de donnée.")
