.. _init:

初始化
==========

初始化的每个可选参数都做了详细说明

::

    # wego 初始化, 对应信息可以登录微信公众平台获取
    w = wego.init(
        # 应用ID
        APP_ID='',
        # 应用密钥
        APP_SECRET='',
        # 注册域名
        REGISTER_URL='http://www.example.com/',
        # WEGO 助手
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


必填参数说明
-------------

    :APP_ID: 应用ID，微信公众平台 -> 开发 -> 基本配置 处获取。

    :APP_SECRET: 应用密钥，微信公众平台 -> 开发 -> 基本配置 处获取。

    :REGISTER_URL: 注册域名, 微信公众平台 -> 接口权限-> 网页授权获取用户基本信息 处填写，在填写域名的基础上需加上 http(s):// 以 / 结尾。

    :HELPER: WEGO 助手，官方助手有：'wego.helpers.DjangoHelper'、'wego.helpers.TornadoHelper' 你也可以参考教程进行自定义：http://wego.quseit.com/customized/helper(building).


.. _pay_options:

微信支付参数说明
--------------------

当需要使用微信参数时，以下参数必填。

    :MCH_ID: 商户号，微信支付|商户平台 -> 账户中心 -> 商户信息 -> 微信支付商户号 处获取。
    
    :MCH_SECRET:  API，密钥 微信支付|商户平台 -> 账户中心 -> 商户信息 -> API 安全 处设置。
    
    :PAY_NOTIFY_PATH: 默认的微信支付通知回调路径，以 / 开头。
    
    :CERT_PEM_PATH: (可选) 证书 apiclient_cert.pem 的路径(建议绝对路径)，需要退款功能时必填，微信支付|商户平台 -> 账户中心 -> 商户信息 -> API 安全 处下载。
    
    :KEY_PEM_PATH: (可选) 证书 apiclient_key.pem 的路径，需要退款功能时必填，下载处同上。


事件推送参数说明
-----------------

当在微信公众平台启用了服务器配置时，以下参数必填。

    :PUSH_TOKEN: 推送令牌 微信公众平台 -> 开发 -> 基本配置 处填写。

    :PUSH_ENCODING_AES_KEY: 消息加解密密钥 微信公众平台 -> 开发 -> 基本配置 处填写。


可选参数说明
-------------

以下参数根据项目需要填写。

    :REDIRECT_PATH: (可选) 强制授权后回跳路径，设置后所有用户授权后都跳转至此。

    :REDIRECT_STATE: (可选) 强制授权后回跳 STATE 值，回跳时固定带上的参数值。

    :GET_GLOBAL_ACCESS_TOKEN: (可选) 定制获取全局 access token 函数，只有分布式系统才需要定制，定制方法：http://wego.quseit.com/customized/GET_GLOBAL_ACCESS_TOKEN(building)。

    :USERINFO_EXPIRE: (可选) 用户信息缓存过期时间，单位秒，默认为 0，subscribe、language、remark 和 groupid 不会被缓存，每次获取仍然会调用 API。
    
    :DEBUG: (可选) 调试模式，默认为 False，为 True 时所有微信支付所需金额为 1 分钱。
    

返回对象
---------

    :return: :class:`WegoApi <wego.api.WegoApi>` object.
