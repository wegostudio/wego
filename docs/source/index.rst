.. wego documentation master file, created by
   sphinx-quickstart on Sat Aug 20 14:49:18 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

WEGO:
================================

Wego 能协助你在微信开发中专注业务逻辑摆脱微信接口调试的烦恼。

起步: ::

    import wego

    # wego 初始化, 对应信息可以登录微信公众平台获取
    w = wego.init(
        # 应用ID (开发 -> 基本配置)
        APP_ID='',
        # 应用密钥 (开发 -> 基本配置)
        APP_SECRET='',
        # 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置
        REGISTER_URL='',
        # WEGO 助手 'wego.helpers.tornado_helper'
        HELPER='wego.helpers.official.DjangoHelper',

        # -- 使用微信支付时才填以下参数 --
        # 商户号
        MCH_ID='',
        # 商户密钥
        MCH_SECRET='',
        # apiclient_cert.pem 证书路径
        CERT_PEM_PATH='/path/to/apiclient_cert.pem',
        # apiclient_key.pem 证书路径
        KEY_PEM_PATH='/path/to/apiclient_key.pem',
        # 微信支付服务器回调路径
        PAY_NOTIFY_PATH='/a/',

        # -- 使用服务器消息推送才填以下参数 --
        # 推送 Token (开发 -> 基本配置)
        PUSH_TOKEN='qbtest',
        # 推送 EncodingAESKey (开发 -> 基本配置)
        PUSH_ENCODING_AES_KEY='IAx51VWAlT5isNH6swoLFaDaX3uhuoL8WVqk3j8W1pN',

        # 选填，微信用户授权登录强制跳转路径, 如 '/'、'/jump'、'/redirect'
        REDIRECT_PATH='/',
        # 选填, 用户信息过期时间, 单位秒
        USERINFO_EXPIRE=60*3,
        # 选填, DEBUG 模式下, 微信支付为 1 分钱
        DEBUG=True,
    )


    # django
    @w.login_required
    def index(request):
        hello = 'Hello {nickname}!'.format(nickname=request.wx_user.nickname)
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