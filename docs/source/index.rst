.. wego documentation master file, created by
   sphinx-quickstart on Sat Aug 20 14:49:18 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

WEGO:
================================

Wego is a dead simple wechat sdk

Usage: ::

    import wego
    w = wego.init(
        # 应用ID
        APP_ID='',

        # 应用密钥
        APP_SECRET='',

        # 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置
        REGISTER_URL='http://www.example.cn/',

        # 微信用户授权登录强制跳转路径, 如 '/'、'/jump'、'/redirect'
        REDIRECT_PATH='/',

        # WEGO 助手 'wego.helpers.tornado_helper'
        HELPER='wego.helpers.official.DjangoHelper',

        # 选填, 商户号 (使用微信支付功能才填)
        MCH_ID='',

        # 选填, 商户密钥 (使用微信支付功能才填)
        MCH_SECRET='',

        # 选填, DEBUG 模式下, 微信支付为 1 分钱, 拥有跟多的 log 信息。
        DEBUG=True,

        # 选填, 用户信息过期时间, 单位秒。
        USERINFO_EXPIRE=10
    )


    # django
    from django.http import HttpResponse

    @w.login_required
    def index(request):
        hello = 'Hello {nickname}!'.format(nickname=request.wx_user.nickname)
        print hello
        # output: Hello your_nickname!
        return HttpResponse(hello)

    # tornado
    class IndexHandler(tornado.web.RequestHandler):
        @w.login_required
        def get(self):
            return 'Hello {nickname}!'.format(nickname=request.wx_user.nickname)

.. toctree::
   :maxdepth: 2

The API Documentation / Guide
-----------------------------

.. toctree::
   :maxdepth: 2

   api