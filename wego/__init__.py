# -*- coding: utf-8 -*-

"""
Wego is a dead simple wechat sdk

usage: ::

    import wego
    w = wego(
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