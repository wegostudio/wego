# -*- coding: utf-8 -*-

"""
wego.settings

default setting
"""

from urllib import quote

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
