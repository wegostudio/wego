# -*- coding: utf-8 -*-

"""
wego.settings

default setting
"""

from urllib import quote
from exceptions import InitError
from wechat import wechat_api

# 应用ID
APP_ID = 'wxe5c3ac08524f5c0f'

# 应用密钥
APP_SECRET = '8e9f505c1764d17c78957f19437065d2'

# 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置
REGISTER_URL = 'http://wx.midoull.com/'

# 微信用户授权登录强制跳转地址，无特殊情况请勿修改
REDIRECT_URL = quote(REGISTER_URL + '')

# 商户号
MCH_ID = '1341134601'

# 商户密钥
MCH_SECRET = 'f093cdd18482fc57ef9755a81073cde3'

# 基本配置 -> 微信事件推送配置
# EVENT_NOTIFY_URL = 'wechat/event-notify'
# EVENT_TOKEN = 'wechat/event-notify'
# EVENT_ENCODING_AES_KEY = 'wechat/event-notify'


def init(**kwargs):

    check_settings(kwargs)

    kwargs['REDIRECT_URL'] = quote(kwargs['REGISTER_URL'] + kwargs['REDIRECT_URL'])
    kwargs['HELPER'] = __import__(kwargs['HELPER'])


    print dir(kwargs['HELPER'])
    print dir(__import__('wego', fromlist=['init']))

    return wechat_api(kwargs)


def check_settings(settings):
    """
    check if settings is available
    .. todo:: serious as same as wechat
    :param settings: dict for settings
    :return: None
    """

    required_list = [
        'APP_ID',
        'APP_SECRET',
        'REGISTER_URL',
        'REDIRECT_URL',
        'HELPER'
    ]

    options_list = [
        ['MCH_ID', 'MCH_SECRET']
    ]

    for i in options_list:
        for j in i:
            if j in settings:
                required_list += i
                break

    for i in required_list:
        if i not in settings or not settings[i]:
            raise InitError('Missing required parameters "{param}"(缺少必须的参数 "{param}")'.format(param=i))

    if not settings['REGISTER_URL'].endswith('/'):
        raise InitError('REGISTER_URL has to ends with "/"(REGISTER_URL 需以 "/" 结尾)')

    if settings['REDIRECT_URL'].startswith('/'):
        raise InitError('REDIRECT_URL can not starts with "/"(REDIRECT_URL 不能以 "/" 打头)')
