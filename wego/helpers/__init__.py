# -*- coding: utf-8 -*-

"""
wego.helpers is compatibility for web framework such as tornado, django and flask

Each file must contain the following functions:

def set_session(request, key, value):
    request.session[key] = value

def get_session(request, key):
    return request.session[key]

def redirect(request, url):
    from django import redirect
    return redirect(url)

"""
