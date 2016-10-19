# -*- coding: utf-8 -*-

"""
wego.settings

default setting
"""

from .exceptions import InitError
import wego
import logging


def init(**kwargs):
    """
    Init settings, get wechat config at https://mp.weixin.qq.com

    :param APP_ID: Wechat AppID get it at basic configuration(基本配置).
    :param APP_SECRET: Wechat AppSecret get it at basic configuration(基本配置).
    :param REGISTER_URL: As same as you set at interface permissions(接口权限)
            >> authorized users obtain basic information page(网页授权获取用户基本信息).
    :param HELPER: Official helper 'wego.helpers.DjangoHelper' and 'wego.helpers.TornadoHelper' or you can customized
            yourself helper with http://wego.quseit.com/customized/helper(building).

    :param MCH_ID: (optional) Mac ID get it at https://pay.weixin.qq.com/ (商户号).
    :param MCH_SECRET: (optional) MCH SECRET As same as you set at https://pay.weixin.qq.com/ (API 密钥).
    :param CERT_PEM_PATH: (optional) Path to apiclient_cert.pem.
    :param KEY_PEM_PATH: (optional) Path to apiclient_key.pem.
    :param PAY_NOTIFY_PATH: (optional) Default notify url for wechat pay callback.

    :param PUSH_TOKEN: (optional) Set at basic configuration(基本配置).
    :param PUSH_ENCODING_AES_KEY: (optional) Set at basic configuration(基本配置).

    :param GET_GLOBAL_ACCESS_TOKEN: (optional) A function that return a global access token, if your application run at
            multiple servers it required. How to customized your GET_GLOBAL_ACCESS_TOKEN:
            http://wego.quseit.com/customized/GET_GLOBAL_ACCESS_TOKEN(building).

    :param USERINFO_EXPIRE: (optional) Set number of seconds expired, default is 0. subscribe,
            language, remark and groupid still is real time.

    :param REDIRECT_PATH: (optional) Default redirect path, redirect when we get user`s authorize.
    :param REDIRECT_STATE: (optional) Default redirect state, redirect when we get user`s authorize.
    :param DEBUG: (optional) Default is True,
            When Debug equal True it will log all information and wechat payment only spend a penny(0.01 yuan).
    :return: :class:`WegoApi <wego.api.WegoApi>` object.
    :rtype: WegoApi.
    """

    default_settings = {
        'GET_GLOBAL_ACCESS_TOKEN': wego.api.official_get_global_access_token,
        'USERINFO_EXPIRE': 0,
        'DEBUG': False
    }
    kwargs = dict(default_settings, **kwargs)

    check_settings(kwargs)

    if 'REDIRECT_STATE' not in kwargs:
        kwargs['REDIRECT_STATE'] = False
    if 'REDIRECT_PATH' not in kwargs:
        kwargs['REDIRECT_PATH'] = False

    if 'PAY_NOTIFY_PATH' in kwargs:
        kwargs['PAY_NOTIFY_URL'] = kwargs['REGISTER_URL'] + kwargs['PAY_NOTIFY_PATH'][1:]

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

    return wego.WegoApi(WegoSettings(kwargs))


def check_settings(settings):
    """
    check if settings is available

    :param settings: a dict.
    :return: None
    """

    required_list = [
        'APP_ID',
        'APP_SECRET',
        'REGISTER_URL',
        'HELPER'
    ]

    # optional_couple
    optional_couple_list = [
        ['MCH_ID', 'MCH_SECRET', 'PAY_NOTIFY_PATH', 'CERT_PEM_PATH', 'KEY_PEM_PATH'],
        ['PUSH_TOKEN', 'PUSH_ENCODING_AES_KEY'],
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

    if 'REDIRECT_PATH' in settings and not settings['REDIRECT_PATH'].startswith('/'):
        raise InitError('REDIRECT_PATH have to starts with "/"(REDIRECT_PATH 需以 "/" 开始)')

    if 'PAY_NOTIFY_PATH' in settings and not settings['PAY_NOTIFY_PATH'].startswith('/'):
        raise InitError('PAY_NOTIFY_PATH have to starts with "/"(PAY_NOTIFY_PATH 需以 "/" 开始)')

    if type(settings['HELPER']) is str:
        modules = settings['HELPER'].split('.')
        settings['HELPER'] = getattr(__import__('.'.join(modules[:-1]), fromlist=['']), modules[-1])

    if not issubclass(settings['HELPER'], wego.helpers.BaseHelper):
        raise InitError('Helper have to inherit the wego.helper.BaseHelper(Helper 必须继承至 wego.helper.BaseHelper)')

    if not hasattr(settings['GET_GLOBAL_ACCESS_TOKEN'], '__call__'):
        raise InitError('GET_GLOBAL_ACCESS_TOKEN is not a function(GET_ACCESS_TOKEN 不是一个函数)')

    # TODO 检查推送消息加解密所需依赖是否安装 PUSH_TOKEN PUSH_ENCODING_AES_KEY

    settings['DEBUG'] = not not settings['DEBUG']


class WegoSettings(object):
    """
    Wego settings
    """

    def __init__(self, data):
        self.data = data

    def __getattr__(self, key):
        if key in self.data:
            return self.data[key]
        return ''

