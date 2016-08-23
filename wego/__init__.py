# -*- coding: utf-8 -*-

"""
Wego is a dead simple wechat sdk
.. todo :: 在线文档对一些错误进行相信说明
.. todo :: 设置初始化的检查应该同微信一样严格
.. todo :: 全局 access token 多次获取只有最后一次有效, 考虑分布式怎么处理这个冲突(允许定制获取access_token的方法)
usage: ::

    import wego
    w = wego.init(
        # 应用ID
        APP_ID = '',

        # 应用密钥
        APP_SECRET = '',

        # 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置
        REGISTER_URL = '',

        # 微信用户授权登录强制跳转路径, 如 '/'、'/jump'、'/redirect'
        REDIRECT_URL = '',
        # REDIRECT_URL = quote(REGISTER_URL + REDIRECT_URL),

        # 商户号
        MCH_ID = '',

        # 商户密钥
        MCH_SECRET = '',

        # WEGO 助手
        # HELPER = 'wego.helpers.tornado_helper'
        HELPER = 'wego.helpers.django_helper'
    )

    # django
    @w.login_required
    def index(request):
        return 'Hello {nickname}!'.format(nickname=request.wx_user.nickname)

    # tornado
    class IndexHandler(tornado.web.RequestHandler):
        @w.login_required
        def get(self):
            return 'Hello {nickname}!'.format(nickname=request.wx_user.nickname)
"""

from settings import init
import wechat
import api
