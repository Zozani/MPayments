#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import unicode_literals, absolute_import, division, print_function
from datetime import datetime
from models import Payment, ProviderOrClient
from playhouse.migrate import (
    BooleanField,
    CharField,
    IntegerField,
    DateTimeField,
)

from Common.cdatabase import AdminDatabase


class Setup(AdminDatabase):

    """docstring for FixtInit"""

    def __init__(self):
        super(AdminDatabase, self).__init__()

        self.LIST_CREAT.append(ProviderOrClient)
        self.LIST_CREAT.append(Payment)
        self.MIG_VERSION = 21
        self.LIST_MIGRATE += [
            ("ProviderOrClient", "deleted", BooleanField(default=False)),
            ("ProviderOrClient", "is_syncro", BooleanField(default=False)),
            ("ProviderOrClient", "devise", CharField(default="xof")),
            ("ProviderOrClient", "phone", IntegerField(null=True)),
            (
                "ProviderOrClient",
                "last_update_date",
                DateTimeField(default=datetime.now),
            ),
            # ('Payment', 'weight', FloatField(null=True)),
            ("Payment", "name", CharField(null=True)),
            ("Payment", "is_syncro", BooleanField(default=False)),
            ("Payment", "last_update_date", DateTimeField(default=datetime.now)),
        ]
