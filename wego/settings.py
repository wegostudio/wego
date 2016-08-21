# -*- coding: utf-8 -*-

"""
wego.settings

default setting
"""

from urllib import quote
from exceptions import InitError
import wego
import logging

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
    """
    Init settings, get wechat config at https://mp.weixin.qq.com
    .. todo:: wego online doc

    :param APP_ID: Wechat AppID get it at basic configuration(基本配置).
    :param APP_SECRET: Wechat AppSecret get it at basic configuration(基本配置).
    :param REGISTER_URL: As same as you set at interface permissions(接口权限)
            >> authorized users obtain basic information page(网页授权获取用户基本信息).
    :param REDIRECT_PATH: Default redirect path, redirect when we get user`s authorize.
    :param HELPER: Official helper 'wego.helpers.django_helper' and 'wego.helpers.tornado_helper' or you can customized
            yourself helper with http://wego.quseit.com/customized/helper(building)

    :param MCH_ID: (optional)
    :param MCH_SECRET: (optional)

    :param DEBUG: (optional) Default is True,
            When Debug equal True it will log all information and wechat payment only spend a penny(0.01 yuan).
    :param LOG_LANGUAGE: (optional) Default is EN only influence logger and exceptions, just support EN and CN,
    :return: :class:`WechatApi <wego.wechat.WechatApi>` object
    :rtype: WechatApi
    """

    check_settings(kwargs)

    kwargs['REDIRECT_URL'] = quote(kwargs['REGISTER_URL'] + kwargs['REDIRECT_PATH'])

    logger = logging.getLogger('wego')
    formatter = logging.Formatter('%(asctime)s - WEGO - %(levelname)s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    if kwargs['DEBUG']:
        logger.setLevel(logging.DEBUG)
        logger.warn(u'\033[1;31mWEGO 运行在 DEBUG 模式, 微信支付付款金额将固定在 1 分钱.\033[0m')

    # logger.debug('debug message')
    # logger.info('info message')
    # logger.warn('warn message')
    # logger.error('error message')
    # logger.critical('critical message')

    return wego.wechat.WechatApi(kwargs)


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
        'REDIRECT_PATH',
        'HELPER'
    ]

    # optional_couple
    optional_couple_list = [
        ['MCH_ID', 'MCH_SECRET'],
    ]

    for i in optional_couple_list:
        for j in i:
            if j in settings:
                required_list += i
                break

    if 'LOG_LANGUAGE' not in settings.keys():
        settings['LANGUAGE'] = 'EN'

    for i in required_list:
        if i not in settings or not settings[i]:
            raise InitError('Missing required parameters "{param}"(缺少必须的参数 "{param}")'.format(param=i))

    if not settings['REGISTER_URL'].endswith('/'):
        raise InitError('REGISTER_URL has to ends with "/"(REGISTER_URL 需以 "/" 结尾)')

    if settings['REDIRECT_PATH'].startswith('/'):
        raise InitError('REDIRECT_URL can not starts with "/"(REDIRECT_URL 不能以 "/" 打头)')

    if type(settings['HELPER']) is str:
        modules = settings['HELPER'].split('.')
        settings['HELPER'] = getattr(__import__('.'.join(modules[:-1]), fromlist=['']), modules[-1])

    if not issubclass(settings['HELPER'], wego.helpers.BaseHelper):
        raise InitError('Helper have to inherit the wego.helper.BaseHelper(Helper 必须继承至 wego.helper.BaseHelper)')

    if 'DEBUG' not in settings.keys():
        settings['DEBUG'] = True
    else:
        settings['DEBUG'] = not not settings['DEBUG']
