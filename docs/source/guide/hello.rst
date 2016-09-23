.. _guide:

Hello world
============

这将是你使用 WEGO 的一个简单起步，放轻松，WEGO 不会给你带来太多理解上的压力，但开始前，我们希望你对 Django 或 Tornado 有一定的使用经验，如果两者你都还没尝试过，我们推荐文档更优秀的 Django 作为你的起步 (https://www.djangoproject.com/)。

初始化
------
我们建议把 wego 的初始化放入你的配置文件内，如 django 的 settings.py，下面所需的参数都可以在微信公众平台获得 (https://mp.weixin.qq.com)。

::

    import wego

    # wego 初始化, 对应信息可以登录微信公众平台获取
    w = wego.init(
        # 应用ID (开发 -> 基本配置)
        APP_ID='',
        # 应用密钥 (开发 -> 基本配置)
        APP_SECRET='',
        # 注册域名, 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置, 需加上 http(s):// 以 / 结尾
        REGISTER_URL='http://www.example.com/',
        # WEGO 助手 'wego.helpers.tornado_helper'
        HELPER='wego.helpers.official.DjangoHelper',
    )

如果你是 tornado 用户，那么我们建议启动 tornado 时配置一下 cookie_secret (http://tornado-zh.readthedocs.io/zh/latest/guide/security.html)，以增强安全性。

::

Hello world
------------
让 wego 和你打个招呼~

::

    # 将上面初始化后的实例 w import 进来
    from somewhere import w

    # django
    @w.login_required
    def index(request):
        hello = 'Hello %s!' % request.wx_user.nickname
        return HttpResponse(hello)

    # tornado
    class IndexHandler(tornado.web.RequestHandler):
        @w.login_required
        def get(self):
            hello = 'Hello %s!' % self.wx_user.nickname
            return self.write(hello)

将 url 指向对应的函数或类，然后访问这个 url，是不是成功了？虽然不是标准的网页没有漂亮的样式字也有些小，但是热情还是在的。

完整参数的初始化
----------------
这是一个使用了当前所有初始化参数的例子。

::

    # wego 初始化, 对应信息可以登录微信公众平台获取
    w = wego.init(
        # 应用ID (开发 -> 基本配置)
        APP_ID='',
        # 应用密钥 (开发 -> 基本配置)
        APP_SECRET='',
        # 注册域名, 微信公众平台左侧: 接口权限-> 网页授权获取用户基本信息内配置, 需加上 http(s):// 以 / 结尾
        REGISTER_URL='http://www.example.com/',
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
        PUSH_TOKEN='',
        # 推送 EncodingAESKey (开发 -> 基本配置)
        PUSH_ENCODING_AES_KEY='',

        # 选填，微信用户授权登录强制跳转路径, 如 '/'、'/jump'、'/redirect'
        REDIRECT_PATH='/',
        # 选填，微信用户授权跳转回来 state 参数的值
        REDIRECT_STATE='/',
        # 选填, 用户信息缓存过期时间, 单位秒, 不填则不缓存用户数据
        USERINFO_EXPIRE=60*3,
        # 选填, DEBUG 模式下, 微信支付为 1 分钱
        DEBUG=True,
    )