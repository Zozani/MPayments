#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QVBoxLayout, QIcon, QTableWidgetItem)

from Common.tabpane import tabbox
from Common.ui.common import FWidget, FPageTitle, FBoxTitle, LineEdit
from Common.ui.table import FTableWidget
from Common.ui.util import show_date, is_int

# from models import Invoice, Buy, ProviderOrClient
from configuration import Config


class DashbordViewWidget(FWidget):

    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(DashbordViewWidget, self).__init__(
            parent=parent, *args, **kwargs)

        self.parentWidget().setWindowTitle(
            Config.APP_NAME + u"    TABLEAU DE BORD")

        self.parent = parent

        vbox = QVBoxLayout()
        table_invoice = QVBoxLayout()
        table_buying = QVBoxLayout()

        self.search_field = LineEdit()
        self.search_field.setPlaceholderText(
            "Taper un nom client ou num. facture")
        self.search_field.setMaximumSize(
            500, self.search_field.maximumSize().height())
        self.search_field.textChanged.connect(self.finder)

        self.title = FPageTitle("TABLEAU DE BORD")

        self.title_buying = FBoxTitle(u"L'arivages ")
        self.table_buying = BuyTableWidget(parent=self)
        table_buying.addWidget(self.title_buying)
        table_buying.addWidget(self.table_buying)

        self.title_invoice = FBoxTitle(u"Les Factures")
        self.table_invoice = InvoiceTableWidget(parent=self)
        table_invoice.addWidget(self.search_field)
        table_invoice.addWidget(self.table_invoice)

        tab_widget = tabbox((table_invoice, u"Factures"),
                            (table_buying, u"Arivages "))

        vbox.addWidget(self.title)
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)

    def finder(self):
        self.table_invoice.refresh_(self.search_field.text())


class InvoiceTableWidget(FTableWidget):

    def __init__(self, parent):
        FTableWidget.__init__(self, parent=parent)
        self.hheaders = [u"Facture N°", u"Date",
                         u"Doit", u"Consulter"]

        self.parent = parent

        self.sorter = True
        self.stretch_columns = [1, 2]
        self.display_fixed = True
        self.align_map = {0: 'r', 1: 'r', 2: 'l', }
        self.refresh_()
        # self.refresh_()

    def refresh_(self, value=None):
        """ """
        self._reset()
        self.set_data_for(value)
        self.refresh()

        pw = self.parent.parent.page_width() / 5
        self.setColumnWidth(0, pw)
        self.setColumnWidth(1, pw)
        self.setColumnWidth(2, pw)

    def set_data_for(self, value):
        try:
            self.data = []
        except Exception as e:
            print("Exception ", e)

    def _item_for_data(self, row, column, data, context=None):
        if column == self.data[0].__len__() - 1:
            return QTableWidgetItem(
                QIcon(u"{img_media}{img}".format(img_media=Config.img_cmedia,
                                                 img="go-next.png")), (u"voir"))

        return super(InvoiceTableWidget, self)._item_for_data(row, column,
                                                              data, context)

    def click_item(self, row, column, *args):
        last_column = self.hheaders.__len__() - 1
        if column != last_column:
            return

        from ui.invoice_show import ShowInvoiceViewWidget
        try:
            self.parent.change_main_context(ShowInvoiceViewWidget,
                                            invoice_num=self.data[row][0])
        except IndexError:
            pass


class BuyTableWidget(FTableWidget):

    def __init__(self, parent, *args, **kwargs):
        FTableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.hheaders = [u"Numéro", u"Date", "Afficher"]

        self.parent = parent
        self.sorter = True
        self.ecart = -35
        self.align_map = {0: 'r', 1: 'l', 2: 'r'}
        self.refresh_()

    def refresh_(self):
        """ """
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = []

    def _item_for_data(self, row, column, data, context=None):
        if column == self.data[0].__len__() - 1:
            return QTableWidgetItem(
                QIcon(u"{img_media}{img}".format(img_media=Config.img_cmedia,
                                                 img="go-next.png")), (u"voir"))

        return super(BuyTableWidget, self)._item_for_data(row, column,
                                                          data, context)

    def click_item(self, row, column, *args):
        last_column = self.hheaders.__len__() - 1
        if column != last_column:
            return
        try:
            from ui.buy_show import BuyShowViewWidget
            self.parent.change_main_context(
                BuyShowViewWidget, buy=Buy.get(id=self.data[row][0]))
        except IndexError:
            pass
