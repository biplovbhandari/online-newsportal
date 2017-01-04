# -*- coding: utf-8 -*-

"""
    Defines the global variables that can be used in model, views and controllers
    
    The current global variables are:
        * app_settings

"""

from collections import OrderedDict
from gluon import current

# Global Settings
app_settings = OrderedDict()
current.app_settings = app_settings

get_vars = request.get_vars
request = current.request
