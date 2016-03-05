#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

from Common.models import (SettingsAdmin, Version,
                           FileJoin, Organization, Owner)
from models import (Payment, ProviderOrClient)


def setup(drop_tables=False):
    """ create tables if not exist """
    did_create = False

    for model in [Payment, Owner, SettingsAdmin, Organization, Version, FileJoin, ProviderOrClient]:
        if drop_tables:
            model.drop_table()
        if not model.table_exists():
            model.create_table()
            did_create = True

    if did_create:
        from fixture import fixt_init
        fixt_init().creat_all_or_pass()

setup()
