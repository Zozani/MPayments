#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fadiga


from PyQt4.QtGui import (QSplitter, QHBoxLayout, QVBoxLayout, QPushButton,
                         QPixmap, QFont, QListWidget, QMenu, QListWidgetItem,
                         QIcon, QFormLayout, QGridLayout)

from datetime import datetime, date
from PyQt4.QtCore import Qt, SIGNAL, SLOT, QSize, QDate

from Common.peewee import fn
from models import ProviderOrClient, Payment

from Common.ui.common import (BttExportXLS, FWidget, FBoxTitle, Button,
                              LineEdit, FLabel, FormatDate, FormLabel)
from Common.ui.table import FTableWidget, TotalsWidget
from Common.ui.util import formatted_number, show_date, is_float, date_to_datetime

from ui.payment_edit_add import EditOrAddPaymentrDialog
from GCommon.ui.provider_client_edit_add import EditOrAddClientOrProviderDialog

from configuration import Config


try:
    unicode
except:
    unicode = str

ALL_CONTACTS = "TOUS"


class DebtsViewWidget(FWidget):

    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DebtsViewWidget, self).__init__(parent=parent,
                                              *args, **kwargs)
        self.parent = parent
        self.parentWidget().setWindowTitle(
            Config.NAME_ORGA + u"Gestion des dettes")

        self.title = u"Movements"

        hbox = QHBoxLayout(self)
        # self.remaining_box = FLabel()
        # self.remaining_box.setMaximumHeight(40)

        self.on_date = FormatDate(
            QDate(date.today().year, date.today().month, 1))
        self.end_date = FormatDate(QDate.currentDate())
        self.now = datetime.now().strftime("%x")
        # self.soldeField = FormLabel("0")
        self.label_balance = FormLabel(u"Solde au {} ".format(self.now))
        self.table = RapportTableWidget(parent=self)
        # self.table = DebtsTableWidget(parent=self)
        self.button = Button(u"Ok")
        self.button.clicked.connect(self.table.refresh_)

        self.btt_export = BttExportXLS(u"Exporter")
        self.btt_export.clicked.connect(self.export_xls)
        self.add_btt = Button("Créditer")
        self.add_btt.setEnabled(False)
        self.add_btt.clicked.connect(self.add_payment)
        self.add_btt.setIcon(QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                              img="in.png")))
        self.sub_btt = Button("Débiter")
        self.sub_btt.setEnabled(False)
        self.sub_btt.clicked.connect(self.sub_payment)
        self.sub_btt.setIcon(QIcon(u"{img_media}{img}".format(img_media=Config.img_media,
                                                              img="out.png")))
        self.add_prov_btt = Button("+ client")
        self.add_prov_btt.setMaximumHeight(60)
        self.add_prov_btt.clicked.connect(self.add_prov_or_clt)
        editbox = QGridLayout()
        # editbox.addWidget(FormLabel(u"Date debut"), 0, 1)
        # editbox.addWidget(self.on_date, 0, 2)
        # editbox.addWidget(FormLabel(u"Date fin"), 1, 1)
        # editbox.addWidget(self.end_date, 1, 2)
        # editbox.addWidget(self.button, 1, 3)
        editbox.addWidget(self.sub_btt, 1, 5)
        editbox.addWidget(self.add_btt, 1, 6)
        editbox.addWidget(self.btt_export, 1, 7)
        editbox.setColumnStretch(1, 4)

        self.table_provid_clt = ProviderOrClientTableWidget(parent=self)

        self.search_field = LineEdit()
        self.search_field.textChanged.connect(self.search)
        self.search_field.setPlaceholderText(u"Nom ou  numéro tel")
        self.search_field.setMaximumHeight(40)
        splitter = QSplitter(Qt.Horizontal)

        self.splitter_right = QSplitter(Qt.Horizontal)
        self.splitter_right.setLayout(editbox)

        self.splitter_left = QSplitter(Qt.Vertical)
        self.splitter_left.addWidget(self.search_field)
        self.splitter_left.addWidget(self.table_provid_clt)
        self.splitter_left.addWidget(self.add_prov_btt)

        splt_clt = QSplitter(Qt.Vertical)
        splt_clt.addWidget(self.splitter_right)
        splt_clt.addWidget(self.table)
        splt_clt.addWidget(self.label_balance)
        splt_clt.resize(900, 1000)
        splitter.addWidget(self.splitter_left)
        splitter.addWidget(splt_clt)

        hbox.addWidget(splitter)
        self.setLayout(hbox)

    def search(self):
        self.table_provid_clt.refresh_(self.search_field.text())

    def add_prov_or_clt(self):
        self.parent.open_dialog(EditOrAddClientOrProviderDialog, modal=True,
                                prov_clt=None, table_p=self.table_provid_clt)

    def export_xls(self):
        from Common.exports_xlsx import export_dynamic_data
        dict_data = {
            'file_name': "versements.xlsx",
            'headers': self.table.hheaders[:-1],
            'data': self.table.data,
            "extend_rows": [(1, self.table.label_mov_tt),
                            (2, self.table.totals_debit),
                            (3, self.table.totals_credit), ],
            "footers": [
                ("C", "E", "Solde au {} = {} {}".format(self.now, self.table.balance_tt, Config.DEVISE)), ],
            'sheet': self.title,
            # 'title': self.title,
            'widths': self.table.stretch_columns,
            'exclude_row': len(self.table.data) - 1,
            "date": "Du {} au {}".format(
                date_to_datetime(self.on_date.text()).strftime(u'%d/%m/%Y'),
                date_to_datetime(self.end_date.text()).strftime(u'%d/%m/%Y'))
        }
        export_dynamic_data(dict_data)

    def add_payment(self):
        self.open_dialog(EditOrAddPaymentrDialog, modal=True,
                         payment=None, type_=Payment.CREDIT, table_p=self.table)

    def sub_payment(self):
        self.open_dialog(EditOrAddPaymentrDialog, modal=True,
                         payment=None, type_=Payment.DEBIT, table_p=self.table)

    def display_remaining(self, text):
        return """ <h2>Solde au {} : <b>{}</b> {} </h2>
               """.format(self.now,  text, Config.DEVISE)


class ProviderOrClientTableWidget(QListWidget):

    """affiche tout le nom de tous les provid_cltes"""

    def __init__(self, parent, *args, **kwargs):
        super(ProviderOrClientTableWidget, self).__init__(parent)

        self.parent = parent
        self.setAutoScroll(True)
        # self.setAutoFillBackground(True)
        self.itemSelectionChanged.connect(self.handleClicked)
        self.refresh_()
        # self.setStyleSheet("QListWidget::item { border-bottom: 1px; }")

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popup)

    def popup(self, pos):
        row = self.selectionModel().selection().indexes()[0].row()
        if row < 1:
            return
        menu = QMenu()
        editaction = menu.addAction("Modifier l'info.")
        action = menu.exec_(self.mapToGlobal(pos))

        provid_clt = ProviderOrClient.get(
            ProviderOrClient.phone == self.item(row).text().split(",")[1])
        if action == editaction:
            self.parent.open_dialog(EditOrAddClientOrProviderDialog, modal=True,
                                    prov_clt=provid_clt, table_p=self)

    def refresh_(self, provid_clt=None):
        """ Rafraichir la liste des provid_cltes"""
        self.clear()
        self.addItem(ProviderOrClientQListWidgetItem(ALL_CONTACTS))
        qs = ProviderOrClient.select().where(
            ProviderOrClient.type_ == ProviderOrClient.CLT)
        if provid_clt:
            qs = qs.where(ProviderOrClient.name.contains(provid_clt))
        for provid_clt in qs:
            self.addItem(ProviderOrClientQListWidgetItem(provid_clt))

    def handleClicked(self):

        self.parent.sub_btt.setEnabled(True)
        self.parent.add_btt.setEnabled(True)
        self.provid_clt = self.currentItem()
        self.parent.table.refresh_(
            provid_clt_id=self.provid_clt.provid_clt_id)


class ProviderOrClientQListWidgetItem(QListWidgetItem):

    def __init__(self, provid_clt):
        super(ProviderOrClientQListWidgetItem, self).__init__()

        self.provid_clt = provid_clt
        self.setSizeHint(QSize(0, 30))
        icon = QIcon()

        if not isinstance(self.provid_clt, str):
            icon.addPixmap(QPixmap("{}.png".format(
                Config.img_media + "debt" if self.provid_clt.is_indebted() else Config.img_cmedia + "user_active")),
                QIcon.Normal, QIcon.Off)

        self.setIcon(icon)
        self.init_text()

    def init_text(self):
        try:
            self.setText(
                "{}, {}".format(self.provid_clt.name, self.provid_clt.phone))
        except AttributeError:
            font = QFont()
            font.setBold(True)
            self.setFont(font)
            self.setTextAlignment(Qt.AlignCenter)
            self.setText(u"Tous")

    @property
    def provid_clt_id(self):
        try:
            return self.provid_clt.id
        except AttributeError:
            return self.provid_clt


class RapportTableWidget(FTableWidget):

    def __init__(self, parent, *args, **kwargs):

        FTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.hheaders = [
            u"Date", u"Libelle opération", u"Débit", u"Crédit", u"Solde", ""]

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popup)

        self.parent = parent

        self.sorter = False
        self.stretch_columns = [0, 1, 2, 3, 4]
        self.align_map = {0: 'l', 1: 'l', 2: 'r', 3: 'r', 4: 'r'}
        self.ecart = -15
        self.display_vheaders = False
        self.refresh_()

    def refresh_(self, provid_clt_id=None, search=None):
        """ """
        l_date = [date_to_datetime(self.parent.on_date.text()),
                  date_to_datetime(self.parent.end_date.text())]
        self._reset()
        self.set_data_for(l_date, provid_clt_id=provid_clt_id, search=search)
        self.refresh()
        self.hideColumn(len(self.hheaders) - 1)

    def set_data_for(self, date_, provid_clt_id=None, search=None):
        self.provid_clt_id = provid_clt_id
        qs = Payment.select().where(
            Payment.status == False).order_by(Payment.date.asc())

        self.remaining = 0
        if isinstance(provid_clt_id, int):
            self.provider_clt = ProviderOrClient.get(id=provid_clt_id)
            qs = qs.select().where(Payment.provider_clt == self.provider_clt)
        else:
            for prov in ProviderOrClient.select().where(
                    ProviderOrClient.type_ == ProviderOrClient.CLT):
                self.remaining += prov.last_remaining()
        self.parent.label_balance.setText(
            self.parent.display_remaining(formatted_number(self.remaining)))

        self.data = [(show_date(pay.date), pay.libelle, pay.debit, pay.credit,
                      pay.balance, pay.id) for pay in qs.iterator()]

    def popup(self, pos):

        # from ui.ligne_edit import EditLigneViewWidget
        from ui.deleteview import DeleteViewWidget
        from data_helper import check_befor_update_payment

        if (len(self.data) - 1) < self.selectionModel().selection().indexes()[0].row():
            return False
        menu = QMenu()
        editaction = menu.addAction("Modifier cette ligne")
        delaction = menu.addAction("Supprimer cette ligne")
        action = menu.exec_(self.mapToGlobal(pos))
        row = self.selectionModel().selection().indexes()[0].row()
        payment = Payment.get(id=self.data[row][-1])
        if action == editaction:
            self.parent.open_dialog(EditOrAddPaymentrDialog, modal=True,
                                    payment=payment, table_p=self)

        if action == delaction:
            self.parent.open_dialog(DeleteViewWidget, modal=True,
                                    table_p=self, obj=payment)

    def extend_rows(self):

        nb_rows = self.rowCount()
        self.setRowCount(nb_rows + 2)
        self.setSpan(nb_rows + 2, 2, 2, 4)
        self.totals_debit = 0
        self.totals_credit = 0
        self.balance_tt = 0
        cp = 0
        for row_num in range(0, self.data.__len__()):
            mtt_debit = is_float(str(self.item(row_num, 2).text()))
            mtt_credit = is_float(str(self.item(row_num, 3).text()))
            # if cp == 0:
            last_balance = is_float(str(self.item(row_num, 4).text()))
            self.totals_debit += mtt_debit
            self.totals_credit += mtt_credit
            cp += 1

        # self.balance_tt = last_balance
        # if isinstance(self.provid_clt_id, str) or not self.provid_clt_id:
        #     self.balance_tt = self.totals_debit - self.totals_credit
        self.balance_tt = self.totals_debit - self.totals_credit

        self.label_mov_tt = u"Totals mouvements: "
        self.setItem(nb_rows, 1, TotalsWidget(self.label_mov_tt))
        self.setItem(
            nb_rows, 2, TotalsWidget(formatted_number(self.totals_debit)))
        self.setItem(
            nb_rows, 3, TotalsWidget(formatted_number(self.totals_credit)))
        self.parent.label_balance.setText(
            self.parent.display_remaining(formatted_number(self.balance_tt)))
