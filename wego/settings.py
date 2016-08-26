# -*- coding: utf-8 -*-

"""
wego.settings

default setting
"""

from urllib import quote
from exceptions import InitError
import wego
import logging
import requests
import time


def init(**kwargs):
    """
    Init settings, get wechat config at https://mp.weixin.qq.com

    :param APP_ID: Wechat AppID get it at basic configuration(基本配置).
    :param APP_SECRET: Wechat AppSecret get it at basic configuration(基本配置).
    :param REGISTER_URL: As same as you set at interface permissions(接口权限)
            >> authorized users obtain basic information page(网页授权获取用户基本信息).
    :param REDIRECT_PATH: Default redirect path, redirect when we get user`s authorize.
    :param HELPER: Official helper 'wego.helpers.django_helper' and 'wego.helpers.tornado_helper' or you can customized
            yourself helper with http://wego.quseit.com/customized/helper(building)

    :param MCH_ID: (optional) Mac ID get it at https://pay.weixin.qq.com/ (商户号)
    :param MCH_SECRET: (optional) MCH SECRET As same as you set at https://pay.weixin.qq.com/ (API 密钥)

    :param GET_GLOBAL_ACCESS_TOKEN: (optional) A function that return a global access token, if your application run at
            multiple servers it required. How to customized your GET_GLOBAL_ACCESS_TOKEN:
            http://wego.quseit.com/customized/GET_GLOBAL_ACCESS_TOKEN(building)

    :param USERINFO_EXPIRE: (optional) Set number of seconds expired, default is 0. subscribe, language, remark and groupid
            still is real time.

    :param DEBUG: (optional) Default is True,
            When Debug equal True it will log all information and wechat payment only spend a penny(0.01 yuan).
    :return: :class:`WegoApi <wego.api.WegoApi>` object
    :rtype: WegoApi
    """

    default_settings = {
        'GET_GLOBAL_ACCESS_TOKEN': wego.api.official_get_global_access_token,
        'USERINFO_EXPIRE': 0,
        'DEBUG': False
    }
    kwargs = dict(default_settings, **kwargs)

    check_settings(kwargs)

    kwargs['REDIRECT_URL'] = quote(kwargs['REGISTER_URL'] + kwargs['REDIRECT_PATH'])

    logger = logging.getLogger('wego')
    formatter = logging.Formatter('%(asctime)s WEGO %(levelname)s: %(message)s', datefmt='%Y/%m/%d %I:%M:%S')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    logger.warn = lambda x: logging.Logger.warn(logger, u'\033[1;31m%s\033[0m' % x)
    if kwargs['DEBUG']:
        logger.setLevel(logging.DEBUG)
        logger.warn(u'WEGO 运行在 DEBUG 模式, 微信支付付款金额将固定在 1 分钱.')
    kwargs['LOGGER'] = logger

    return wego.api.WegoWrapper(WegoSettings(kwargs))


def check_settings(settings):
    """
    check if settings is available

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

    for i in required_list:
        if i not in settings or not settings[i]:
            raise InitError('Missing required parameters "{param}"(缺少必须的参数 "{param}")'.format(param=i))

    if not settings['REGISTER_URL'].endswith('/'):
        raise InitError('REGISTER_URL has to ends with "/"(REGISTER_URL 需以 "/" 结尾)')

    if not settings['REDIRECT_PATH'].startswith('/'):
        raise InitError('REDIRECT_URL have to starts with "/"(REDIRECT_URL 需以 "/" 开始)')

    if type(settings['HELPER']) is str:
        modules = settings['HELPER'].split('.')
        settings['HELPER'] = getattr(__import__('.'.join(modules[:-1]), fromlist=['']), modules[-1])

    if not issubclass(settings['HELPER'], wego.helpers.BaseHelper):
        raise InitError('Helper have to inherit the wego.helper.BaseHelper(Helper 必须继承至 wego.helper.BaseHelper)')

    if not hasattr(settings['GET_GLOBAL_ACCESS_TOKEN'], '__call__'):
        raise InitError('GET_GLOBAL_ACCESS_TOKEN is not a function(GET_ACCESS_TOKEN 不是一个函数)')

    settings['DEBUG'] = not not settings['DEBUG']


class WegoSettings(object):
    """
    Wego settings
    """

    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        return self.data[key]

