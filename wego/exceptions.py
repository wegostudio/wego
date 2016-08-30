# -*- coding: utf-8 -*-

"""
wego.exceptions

This module contains the set of wego' exceptions.
"""


class InitError(Exception):
    """An init error occurred."""


class HelperError(Exception):
    """An helper error occurred."""


class WeChatApiError(Exception):
    """An wechat api error occurred."""


class WegoApiError(Exception):
    """An wego api error occurred."""


class WeChatUserError(Exception):
    """An wechat user error occurred."""


class WeChatButtonError(Exception):
    """An wechat button error occurred."""
