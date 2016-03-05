#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import (unicode_literals, absolute_import, division,
                        print_function)

import os
import sys
sys.path.append(os.path.abspath('../'))


from Common.fixture import AdminFixture


class fixt_init(AdminFixture):

    """docstring for fixt_init"""

    def __init__(self):
        super(AdminFixture, self).__init__()
