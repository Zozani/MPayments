#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from Common.fixture import AdminFixture

sys.path.append(os.path.abspath("../"))


class FixtInit(AdminFixture):

    """docstring for FixtInit"""

    def __init__(self):
        super(AdminFixture, self).__init__()
