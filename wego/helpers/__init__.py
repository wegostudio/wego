# -*- coding: utf-8 -*-

"""
wego.helpers is compatibility for web framework such as tornado, django and flask

Each helper must contain the following functions:

class YourHelper(wego.helper.BaseHelper):

    def wego_get_current_url(self, request):
        pass

    def wego_set_session(self, request, key, value):
        pass

    def wego_get_session(self, request, key):
        pass

    def wego_redirect(self, request, url):
        pass

"""

from .base_helper import BaseHelper
