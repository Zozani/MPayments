#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from datetime import datetime, date

from PyQt4.QtGui import (QVBoxLayout, QGridLayout,  QFormLayout, QIcon, QMenu)
from PyQt4.QtCore import Qt, QDate

from configuration import Config
from Common.ui.common import (FormLabel, FWidget, FPeriodHolder, FPageTitle,
                              Button, BttExportXLS, FormatDate, ExtendedComboBox)
from Common.ui.table import FTableWidget, TotalsWidget
from Common.ui.util import device_amount, is_float, show_date, date_to_datetime
from models import Payment, ProviderOrClient
from ui.payment_edit_add import EditOrAddPaymentrDialog


try:
    unicode
except:
    unicode = str


class StatisticsViewWidget(FWidget, FPeriodHolder):

    def __init__(self, parent=0, *args, **kwargs):

        super(StatisticsViewWidget, self).__init__(
            parent=parent, *args, **kwargs)
        FPeriodHolder.__init__(self, *args, **kwargs)

        self.parent = parent

        self.title = u"Movements"

        self.on_date_field = FormatDate(
            QDate(date.today().year, date.today().month, 1))
        self.end_date_field = FormatDate(QDate.currentDate())
        self.now = datetime.now().strftime(Config.DATEFORMAT)
        self.soldeField = FormLabel(device_amount(0))
        balanceBox = QGridLayout()
        balanceBox.addWidget(self.soldeField, 0, 3)
        balanceBox.setColumnStretch(0, 1)

        self.string_list = [""] + ["{},{}".format(clt.name, clt.phone)
                                   for clt in ProviderOrClient.select().where(
            ProviderOrClient.type_ == ProviderOrClient.CLT).order_by(ProviderOrClient.name.desc())]

        self.name_client_field = ExtendedComboBox()
        self.name_client_field.addItems(self.string_list)
        self.name_client_field.setMaximumSize(
            200, self.name_client_field.maximumSize().height())
        self.name_client_field.setToolTip("Nom, numero du client")

        self.table = RapportTableWidget(parent=self)
        self.button = Button(u"Ok")
        self.button.clicked.connect(self.refresh_prov_clt)

        formbox_period = QFormLayout()
        self.btt_export = BttExportXLS(u"Exporter")
        self.btt_export.clicked.connect(self.export_xls)

        editbox = QGridLayout()
        editbox.addWidget(FormLabel(u"Date debut"), 0, 1)
        editbox.addWidget(self.on_date_field, 0, 2)
        editbox.addWidget(FormLabel(u"Date fin"), 1, 1)
        editbox.addWidget(self.end_date_field, 1, 2)
        editbox.addWidget(self.name_client_field, 0, 3)
        editbox.addWidget(self.button, 1, 3)
        editbox.addWidget(self.btt_export, 1, 7)
        editbox.setColumnStretch(4, 2)

        vbox = QVBoxLayout()
        vbox.addWidget(FPageTitle(self.title))
        vbox.addLayout(formbox_period)
        vbox.addLayout(editbox)
        vbox.addWidget(self.table)
        vbox.addLayout(balanceBox)
        self.setLayout(vbox)

    def refresh_prov_clt(self):

        try:
            self.name_client, self.phone = self.name_client_field.lineEdit().text().split(",")
            clt = ProviderOrClient.get(phone=int(self.phone.replace(" ", "")))
            self.table.refresh_(provid_clt_id=clt.id)
        except Exception as e:
            self.table.refresh_()
            print(" ", e)

    def export_xls(self):
        from Common.exports_xlsx import export_dynamic_data
        dict_data = {
            'file_name': "versements.xlsx",
            'headers': self.table.hheaders[:-1],
            'data': self.table.data,
            "extend_rows": [(1, self.table.label_mov_tt),
                            (2, self.table.totals_debit),
                            (3, self.table.totals_credit), ],
            "footers": [("C", "E", "Solde du {} au {} = {}".format(
                self.table.on_date, self.table.end_date, device_amount(self.table.balance_tt))), ],
            'sheet': self.title,
            # 'title': self.title,
            'widths': self.table.stretch_columns,
            'format_money': ["C:C", "D:D", "E:E", ],
            # 'exclude_row': len(self.table.data) - 1,
            'others': [("A7", "C7", "Compte : {}".format(self.table.provider_clt)), ],
            # "date": "Du {} au {}".format(self.table.on_date, self.table.end_date)
        }
        export_dynamic_data(dict_data)

    def display_remaining(self, amount_text):
        return """ <h2>Solde du {}: <b>{}</b></h2>
               """.format(self.now, amount_text)


class RapportTableWidget(FTableWidget):

    def __init__(self, parent, *args, **kwargs):

        FTableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.hheaders = [
            u"Date", u"Libelle opération", u"Débit", u"Crédit", u"Solde", ""]

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.popup)

        self.parent = parent

        self.sorter = True
        self.stretch_columns = [0, 1, 2, 3, 4]
        self.align_map = {0: 'l', 1: 'l', 2: 'r', 3: 'r', 4: 'r'}
        # self.ecart = -5
        self.display_vheaders = False
        self.refresh_()

    def refresh_(self, provid_clt_id=None, search=None):
        """ """

        self.totals_debit = 0
        self.totals_credit = 0
        self.balance_tt = 0
        self.on_date = date_to_datetime(self.parent.on_date_field.text())
        self.end_date = date_to_datetime(self.parent.end_date_field.text())

        l_date = [self.on_date, self.end_date]
        self._reset()
        self.set_data_for(l_date, provid_clt_id=provid_clt_id, search=search)
        self.refresh()

        self.parent.soldeField.setText(
            self.parent.display_remaining(device_amount(self.balance_tt)))

        self.hideColumn(len(self.hheaders) - 1)

    def set_data_for(self, date_, provid_clt_id=None, search=None):
        self.provid_clt_id = provid_clt_id
        qs = Payment.select().where(
            Payment.status == False).order_by(Payment.date.asc())
        if isinstance(self.provid_clt_id, int):
            self.provider_clt = ProviderOrClient.get(id=self.provid_clt_id)
            qs = qs.select().where(Payment.provider_clt == self.provider_clt)
        else:
            self.provider_clt = "Tous"

        self.data = [(pay.date, pay.libelle, pay.debit, pay.credit,
                      pay.balance, pay.id) for pay in qs.filter(Payment.date > date_[
                          0], Payment.date < date_[1]).order_by(Payment.date.asc())]

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
        cp = 0
        for row_num in range(0, self.data.__len__()):
            mtt_debit = is_float(unicode(self.item(row_num, 2).text()))
            mtt_credit = is_float(unicode(self.item(row_num, 3).text()))
            if cp == 0:
                last_balance = is_float(unicode(self.item(row_num, 4).text()))
            self.totals_debit += mtt_debit
            self.totals_credit += mtt_credit
            cp += 1

        # self.balance_tt = last_balance
        self.balance_tt = self.totals_credit - self.totals_debit

        self.label_mov_tt = u"Totals mouvements: "
        self.setItem(nb_rows, 1, TotalsWidget(self.label_mov_tt))
        self.setItem(
            nb_rows, 2, TotalsWidget(device_amount(self.totals_debit)))
        self.setItem(
            nb_rows, 3, TotalsWidget(device_amount(self.totals_credit)))
