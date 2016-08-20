# -*- coding: utf-8 -*-


def set_session(request, key, value):
    request.session[key] = value


def get_session(request, key):
    return request.session[key]


def redirect(request, url):
    from django.shortcuts import redirect
    return redirect(url)