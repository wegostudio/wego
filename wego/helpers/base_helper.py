# -*- coding: utf-8 -*-
from wego.exceptions import HelperError


class BaseHelper(object):
    """
    wego base helper, any helper have to inherit this.
    """

    def get_current_url(self, request):
        raise HelperError('you have to customized YourHelper.get_current_url')

    def set_session(self, request, key, value):
        raise HelperError('you have to customized YourHelper.set_session')

    def get_session(self, request, key):
        raise HelperError('you have to customized YourHelper.get_session')

    def redirect(self, request, url):
        raise HelperError('you have to customized YourHelper.redirect')
