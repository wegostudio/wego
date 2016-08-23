# -*- coding: utf-8 -*-

"""
wego.exceptions

This module contains the set of wego' exceptions.
"""


class InitError(Exception):
    u"""An init error occurred."""


class HelperError(Exception):
    u"""An helper error occurred."""


class WeChatApiError(Exception):
    u"""An wechat api error occurred."""


class WeChatUserError(Exception):
    u"""An wechat user error occurred."""
