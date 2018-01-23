#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division,
                        print_function)
import os
# from static import Constants
from Common.cstatic import CConstants
# from Common.models import Organization

ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))


class Config(CConstants):

    """ docstring for Config
                            """

    DATEFORMAT = u'%d-%m-%Y'

    def __init__(self):
        CConstants.__init__(self)

    # ------------------------- Organisation --------------------------#

    DEBUG = False
    DEVISEPEPROV = True
    # DEVISEPEPROV = False

    # des_image_record = "static/img_prod"
    ARMOIRE = "img_prod"
    des_image_record = os.path.join(ROOT_DIR, ARMOIRE)
    PEEWEE_V = 224
    credit = 17
    tolerance = 50
    nb_warning = 5
    ORG_LOGO = None

    # -------- Application -----------#

    NAME_MAIN = "main.py"

    pdf_source = "pdf_source.pdf"
    APP_NAME = "MPayments"
    APP_VERSION = 1
    APP_DATE = u"11/2017"
    img_media = os.path.join(os.path.join(ROOT_DIR, "static"), "images/")
    APP_LOGO = os.path.join(img_media, "logo.png")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")

    # org = Organization.get(id=1)
    # NAME_ORGA = org.name_orga
    # CONTACT_ORGA = u"Bamako-Rep. du Mali"
    # TEL_ORGA = org.phone
    # ADRESS_ORGA = org.adress_org
    # BP = org.bp
    # EMAIL_ORGA = org.email_org
    # DEVISE_M = org.devise
