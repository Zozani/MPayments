#!/usr/bin/env python
# -*- encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from Common.ui.util import formatted_number


def check_befor_update_payment(pay):
    from models import Payment

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


def device(value, provider, dvs=None):

    from models import ProviderOrClient
    if dvs:
        return "{} {}".format(formatted_number(value), dvs)
    try:
        if isinstance(provider, int):
            provider = ProviderOrClient().get(id=int(provider))
        else:
            provider = provider
    except Exception as e:
        print(e)
    d = provider.DEVISE[provider.devise]
    v = formatted_number(value)
    if provider.devise == provider.USA:
        return "{d}{v}".format(v=v, d=d)
    else:
        return "{v} {d}".format(v=v, d=d)
