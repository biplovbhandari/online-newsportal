# -*- coding: utf-8 -*-

"""
    Define the tables
"""

from authentication import Authentication

# Auth Tables
current.auth = auth = Authentication()

auth.define_tables(migrate=migrate, fake_migrate=fake_migrate)
