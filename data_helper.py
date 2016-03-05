#!/usr/bin/env python
# -*- encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from models import Payment
from configuration import Config


def check_befor_update_payment(pay):
    balance = pay.balance
    lt = []
    for rpt in pay.next_rpts():
        previous_balance = int(rpt.last_balance_payment())
        if rpt.type_ == Payment.CREDIT:
            balance = previous_balance + int(rpt.credit)
            lt.append(
                "{} = last {} + {}".format(balance, previous_balance, rpt.credit))
        if rpt.type_ == Payment.DEBIT:
            balance = previous_balance - int(rpt.debit)
            lt.append(
                "{} = last {} - {}".format(balance, previous_balance, rpt.debit))
        # if balance < 0:
        #     return False
    return True
