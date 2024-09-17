#!/usr/bin/env python
# -*- coding: utf-8 -*-
# maintainer: Fad
from __future__ import absolute_import, division, print_function, unicode_literals

from Common.ui.common import (
    Button,
    FBoxTitle,
    FormatDate,
    FormLabel,
    FPageTitle,
    FWidget,
    IntLineEdit,
)
from Common.ui.util import check_is_empty, date_to_datetime, raise_success
from data_helper import check_befor_update_data
from models import Product, Report
from PyQt5.QtCore import QDate, QTime, QVariant
from PyQt5.QtWidgets import (
    QComboBox,
    QDateTimeEdit,
    QDialog,
    QFormLayout,
    QIntValidator,
    QVBoxLayout,
)

try:
    unicode
except:
    unicode = str


class EditLigneViewWidget(QDialog, FWidget):
    def __init__(self, table_p, report, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.setWindowTitle("Modification")
        self.table_p = table_p
        self.rpt = report
        self.parent = parent

        self.out_op = True
        if self.rpt.type_ == Report.E:
            self.out_op = False

        self.selling_price_field = IntLineEdit(unicode(self.rpt.selling_price))
        self.cost_buying_field = IntLineEdit(unicode(self.rpt.cost_buying))
        self.qty_field = IntLineEdit(unicode(self.rpt.qty))

        self.date_field = FormatDate(QDate(self.rpt.date))
        self.date_field.setEnabled(False)

        butt = Button("Mise à jour")
        butt.clicked.connect(self.edit_report)
        cancel_but = Button("Annuler")
        cancel_but.clicked.connect(self.cancel)

        # Combobox widget
        i = 0
        self.liste_type = [Report.E, Report.S]
        self.box_type = QComboBox()
        self.box_type.setEnabled(False)
        for index in xrange(0, len(self.liste_type)):
            ty = self.liste_type[index]
            if ty == self.rpt.type_:
                i = index
            sentence = "%(ty)s" % {"ty": ty}
            self.box_type.addItem(sentence, ty)
            self.box_type.setCurrentIndex(i)
        # Combobox widget
        # self.liste_store = Store.order_by(desc(Store.id)).all()
        # self.box_mag = QComboBox()
        # for index in xrange(0, len(self.liste_store)):
        #     op = self.liste_store[index]
        #     sentence = u"%(name)s" % {'name': op.name}
        #     self.box_mag.addItem(sentence, QVariant(op.id))
        # Combobox widget

        self.liste_product = Product.all()
        self.box_prod_field = QComboBox()
        self.box_prod_field.setEnabled(False)

        for index in xrange(0, len(self.liste_product)):
            prod = self.liste_product[index]
            if prod.name == self.rpt.product.name:
                i = index
            sentence = "%(name)s" % {"name": prod.name}
            self.box_prod_field.addItem(sentence, prod.id)
            self.box_prod_field.setCurrentIndex(i)
        vbox = QVBoxLayout()
        formbox = QFormLayout()
        # editbox.addWidget(FormLabel((_(u"Store"))), 0, 1)
        # editbox.addWidget(self.box_mag, 1, 1)
        formbox.addRow(FormLabel("Type"), FormLabel(self.rpt.type_))
        formbox.addRow(FormLabel("Désignation"), self.box_prod_field)
        formbox.addRow(FormLabel("Quantité"), self.qty_field)
        formbox.addRow(FormLabel("Prix d'achat"), self.cost_buying_field)
        formbox.addRow(FormLabel("Prix vente"), self.selling_price_field)
        formbox.addRow(FormLabel("Date"), self.date_field)
        formbox.addRow(butt, cancel_but)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_report(self):
        # type_ = self.box_type.currentIndex()
        # product = self.liste_product[self.box_prod.currentIndex()]
        if check_is_empty(self.qty_field):
            return
        if check_is_empty(self.selling_price_field):
            return
        if check_is_empty(self.cost_buying_field):
            return
        report = self.rpt
        report.qty = unicode(self.qty_field.text())
        report.selling_price = unicode(self.selling_price_field.text())
        report.cost_buying = unicode(self.cost_buying_field.text())
        try:
            report.save()
            self.cancel()
            self.table_p.refresh_()
            self.parent.Notify("le rapport a été mise à jour", "success")
        except Exception as e:
            self.parent.Notify(e, "error")
