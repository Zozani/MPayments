#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fadiga

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from datetime import datetime

from Common.peewee import (DateTimeField, CharField, IntegerField, BooleanField,
                           ForeignKeyField, TextField)
from Common.models import (BaseModel, SettingsAdmin, Version, FileJoin,
                           Organization, Owner)

FDATE = u"%c"
NOW = datetime.now()


class ProviderOrClient(BaseModel):

    """ Represents the company emmiting the invoices
    """
    # class Meta:
    #     order_by = ('name',)

    CLT = 'Client'
    FSEUR = 'Fournisseur'
    TYPES = [CLT, FSEUR]

    name = CharField(verbose_name=("Nom de votre entreprise"))
    address = TextField(
        null=True, verbose_name=("Adresse principale de votre société"))
    phone = IntegerField(
        unique=True, verbose_name=("Numero de téléphone de votre entreprise"))
    email = CharField(
        null=True, verbose_name=("Adresse électronique de votre entreprise"))
    legal_infos = TextField(
        null=True, verbose_name=("Informations légales"))
    type_ = CharField(max_length=30, choices=TYPES, default=CLT)
    picture = ForeignKeyField(
        FileJoin, null=True, related_name='file_joins_pictures', verbose_name=("image de la societe"))

    def invoices(self):
        return Invoice.select().where(Invoice.client == self)

    def buys(self):
        return Buy.select().where(Buy.provd_or_clt == self)

    def invoices_items(self):
        return Report.select().where(Report.type_ == Report.S,
                                     Report.invoice.client == self)

    def is_indebted(self):
        flag = False
        if self.last_remaining() > 0:
            flag = True
        return flag

    def last_refund(self):
        try:
            return Refund.select().where(Refund.provider_client == self).order_by(
                Refund.date.desc()).get()
        except Exception as e:
            return None

    def last_remaining(self):
        last_r = self.last_refund()
        return last_r.remaining if last_r else 0

    def __str__(self):
        return u"{}, {}".format(self.name, self.phone)

    def __unicode__(self):
        return self.__str__()

    @classmethod
    def get_or_create(cls, name, phone, typ):
        try:
            ctct = cls.get(name=name, phone=phone, type_=typ)
        except cls.DoesNotExist:
            ctct = cls.create(name=name, phone=phone, type_=typ)
        return ctct


class Payment(BaseModel):

    """ docstring for Payment """

    class Meta:
        order_by = ('date',)

    DEBIT = "Debit"
    CREDIT = "Credit"

    DC = [DEBIT, CREDIT]

    owner = ForeignKeyField(Owner, verbose_name=("Utilisateur"))
    provider_clt = ForeignKeyField(ProviderOrClient)
    date = DateTimeField(verbose_name=("Date"))
    debit = IntegerField(verbose_name=("Débit"))
    credit = IntegerField(verbose_name=("Crédit"))
    libelle = CharField(verbose_name=("Libelle"), null=True)
    balance = IntegerField(verbose_name=("Solde"))
    type_ = CharField(choices=DC)
    deleted = BooleanField(default=False)
    status = BooleanField(default=False)

    def __unicode__(self):
        return "Le {date} {type_} d'un montant de {amount} Fcfa".format(
            date=self.date.strftime(FDATE), type_=self.type_,
            amount=self.credit if self.type_ == self.CREDIT else self.debit, lib=self.libelle)

    def __str__(self):
        return self.__unicode__()

    def display_name(self):
        return self.__unicode__()

    def save(self):
        """
        Calcul du balance en stock après une operation."""
        self.owner = Owner.get(Owner.islog == True)
        print("SAVE BEGIN")
        previous_balance = int(
            self.last_balance_payment().balance if self.last_balance_payment() else 0)
        if self.type_ == self.CREDIT:
            self.balance = previous_balance + int(self.credit)
            self.debit = 0
        if self.type_ == self.DEBIT:
            self.balance = previous_balance - int(self.debit)
            self.credit = 0

        super(Payment, self).save()

        if self.next_rpt():
            self.next_rpt().save()

    def next_rpt(self):
        try:
            return self.next_rpts().get()
        except Exception as e:
            print("next_rpt", e)
            return None

    def next_rpts(self):
        try:
            return Payment.select().where(Payment.provider_clt == self.provider_clt,
                                          Payment.date > self.date, Payment.deleted == False).order_by(Payment.date.asc())
        except Exception as e:
            return None
            print("next_rpt", e)

    def deletes_data(self):
        last = self.last_balance_payment()
        next_ = self.next_rpt()
        self.delete_instance()
        if last:
            last.save()
        else:
            if next_:
                next_.save()
        return

    def last_balance_payment(self):
        try:
            return Payment.select().where(Payment.provider_clt == self.provider_clt,
                                          Payment.deleted == False, Payment.date < self.date).order_by(Payment.date.desc()).get()
        except Exception as e:
            print("last_balance_payment", e)
            return None

# class Refund(BaseModel):

#     class Meta:
#         order_by = ('date',)

#     """docstring for ClassName"""
#     DT = "D"
#     RB = "R"

#     owner = ForeignKeyField(Owner, verbose_name=("Utilisateur"))
#     provider_client = ForeignKeyField(ProviderOrClient)
#     date = DateTimeField(default=NOW)
#     invoice = ForeignKeyField(Invoice, null=True)
#     amount = IntegerField(verbose_name="Montant")
#     remaining = IntegerField(verbose_name="Reste à payer")
#     type_ = CharField(verbose_name="Type d'opération")
#     # "fin de payement"
#     status = BooleanField(default=False)
#     deleted = BooleanField(default=False)

#     def __str__(self):
#         return "{owner}{amount}{date}".format(
#             owner=self.owner, date=self.date, amount=self.amount)

#     def __unicode__(self):
#         return self.__str__()

#     def display_name(self):
#         return self.__str__()

#     def save(self):
#         """
#         Calcul du remaining en stock après une operation."""
#         self.owner = Owner.get(Owner.islog == True)
#         print("SAVE BEGIN")
#         previous_remaining = int(
#             self.last_refund().remaining if self.last_refund() else 0)
#         if self.type_ == self.RB:
#             self.remaining = previous_remaining - int(self.amount)
#         if self.type_ == self.DT:
#             self.remaining = previous_remaining + int(self.amount)

#         super(Refund, self).save()

#         if self.next_rpt():
#             self.next_rpt().save()

#     def next_rpt(self):
#         try:
#             return self.next_rpts().get()
#         except:
#             return None

#     def next_rpts(self):
#         try:
#             return Refund.select().where(
#                 Refund.date > self.date,
#                 Refund.provider_client == self.provider_client,
#                 Refund.deleted == False).order_by(Refund.date.asc())
#         except Exception as e:
#             return None
#             print("next_rpt", e)

#     def deletes_data(self):
#         last = self.last_refund()
#         next_ = self.next_rpt()
#         self.delete_instance()
#         if last:
#             last.save()
#         else:
#             if next_:
#                 next_.save()
#         return

#     def last_refund(self):
#         try:
#             return self.all_refund_by_clt_prov().where(
#                 Refund.date < self.date).order_by(Refund.date.desc()).get()
#         except Exception as e:
#             print("last_balance_payment", e)
#             return None

#     def all_refund_by_clt_prov(self):
#         return Refund.select().where(
#             Refund.deleted == False,
#             Refund.provider_client == self.provider_client)

#     def refund_remaing(self):
# return
# self.all_refund_by_clt_prov().order_by(Refund.date.desc()).get().remaining
