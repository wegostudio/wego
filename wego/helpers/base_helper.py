# -*- coding: utf-8 -*-
from wego.exceptions import HelperError


class BaseHelper(object):
    """
    wego base helper, any helper have to inherit this.
    """

    def get_current_path(self):
        raise HelperError('you have to customized YourHelper.get_current_path')

    def get_params(self):
        raise HelperError('you have to customized YourHelper.get_params')

    def get_body(self):
        raise HelperError('you have to customized YourHelper.get_body')

    def set_session(self, key, value):
        raise HelperError('you have to customized YourHelper.set_session')

    def get_session(self, key):
        raise HelperError('you have to customized YourHelper.get_session')

    def redirect(self, url):
        raise HelperError('you have to customized YourHelper.redirect')
