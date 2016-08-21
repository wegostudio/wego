# -*- coding: utf-8 -*-

"""
wego.helpers is compatibility for web framework such as tornado, django and flask

Each file must contain the following functions:

def set_session(request, key, value):
    # request.session[key] = value
    pass

def get_session(request, key):
    # return request.session[key]
    pass

# from django import redirect
def redirect(request, url):
    # return redirect(url)
    pass

"""

from base_helper import BaseHelper
