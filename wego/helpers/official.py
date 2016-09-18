# -*- coding: utf-8 -*-
from base_helper import BaseHelper


class DjangoHelper(BaseHelper):

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
