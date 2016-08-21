# -*- coding: utf-8 -*-
from wego.exceptions import HelperError


class BaseHelper(object):
    """
    wego base helper, any helper have to inherit this.
    """

    def wego_get_current_url(self, request):
        raise HelperError('you have to customized wego_get_current_url')

    def wego_set_session(self, request, key, value):
        raise HelperError('you have to customized wego_set_session')

    def wego_get_session(self, request, key):
        raise HelperError('you have to customized wego_get_session')

    def wego_redirect(self, request, url):
        raise HelperError('you have to customized wego_redirect')
