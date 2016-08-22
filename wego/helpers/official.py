# -*- coding: utf-8 -*-
from base_helper import BaseHelper


class DjangoHelper(BaseHelper):

    def wego_get_current_path(self, request):
        return request.get_full_path()

    def wego_get_params(self, request):
        return request.GET.dict()

    def wego_set_session(self, request, key, value):
        return request.session.get(key, False)

    def wego_get_session(self, request, key):
        return request.session[key]

    def wego_redirect(self, request, url):
        from django.shortcuts import redirect
        return redirect(url)