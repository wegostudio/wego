# -*- coding: utf-8 -*-
from .base_helper import BaseHelper


class DjangoHelper(BaseHelper):

    def __init__(self, request):
        self.request = request

    def get_current_path(self):
        return self.request.get_full_path()

    def get_params(self):
        return self.request.GET.dict()

    def get_body(self):
        return self.request.body

    def set_session(self, key, value):
        self.request.session[key] = value

    def get_session(self, key):
        return self.request.session.get(key, False)

    def redirect(self, url):
        from django.shortcuts import redirect
        return redirect(url)


class TornadoHelper(BaseHelper):

    def __init__(self, handler):
        self.handler = handler
        self.session = {}
        if 'cookie_secret' not in handler.settings:
            handler.settings['cookie_secret'] = 'wego,herewego'

    def get_current_path(self):
        return self.handler.request.uri

    def get_params(self):
        return {i: j[-1] for i, j in self.handler.request.arguments.items()}

    def get_body(self):
        return self.handler.request.body

    def set_session(self, key, value):
        self.session[key] = value
        self.handler.set_secure_cookie(key, value)

    def get_session(self, key):
        if key in self.session:
            return self.session[key]
        return self.handler.get_secure_cookie(key)

    def redirect(self, url):
        return self.handler.redirect(url)


