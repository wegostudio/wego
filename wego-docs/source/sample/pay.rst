.. _pay:

微信支付
==========

微信的支付方式有多种，目前 wego 只实现了公众号支付、扫码支付，其他支付方式正在开发中...


准备工作
-------------

初始化生成 w 实例时，请记得将所需参数填入，详细参数请看 :ref:`pay_options`


公众号支付
----------------

在 wego，你只需要填入对应的参数(详细参数查看 `微信统一下单API <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1>`_ )，即可生成前端调起微信支付所需的 json 数据，下面是一个访问便立即调起微信支付的django示例。

::

    # Django
    @w.login_required
    def wechat_pay(request):
        import time
        order = 'ordernum' + str(int(time.time()))
        raw_html = json.dumps(w.unified_order(
            openid=request.wx_openid,
            body='test',
            out_trade_no= order,
            total_fee='1',
            spbill_create_ip='113.16.139.82',
            trade_type='JSAPI',
        ))

        return render('pay.html', {'data': raw_html})

    # H5调起支付API
    '''
    <script>
        document.getElementById('payBtn').onclick = function () {
            // 调用微信支付接口
            var data = {{data|safe}};
            function onBridgeReady () {
                WeixinJSBridge.invoke(
                    'getBrandWCPayRequest', data, function (res) {
                        if(res.err_msg == "get_brand_wcpay_request：ok" ) {
                            // TODO
                        }
                    }
                );
            }
            if (typeof WeixinJSBridge == "undefined") {
                if (document.addEventListener) {
                    document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
                } else if (document.attachEvent) {
                    document.attachEvent('Weix1inJSBridgeReady', onBridgeReady); 
                    document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
                }
            } else {
                onBridgeReady();
            }
        }
    </script>
    '''

必要参数说明
^^^^^^^^^^^^^^
    :openid: openid如何获取，可参考 `【获取openid】 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_4>`_ 。企业号请使用【企业号OAuth2.0接口】获取企业号内成员userid，再调用【企业号userid转openid接口】进行转换
    :body: 商品简单描述，该字段须严格按照规范传递，具体请见 `参数规定 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_
    :out_trade_no: 商户系统内部的订单号,32个字符内、可包含字母, 其他说明见 `商户订单号 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_
    :total_fee: 订单总金额，单位为分，详见 `支付金额 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_
    :spbill_create_ip: APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP。
    :trade_type: 取值如下：JSAPI，NATIVE，APP，详细说明见 `参数规定 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_

可选参数说明
^^^^^^^^^^^^^^^
    :device_data: 终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
    :detail: 商品详细列表，使用Json格式，传输签名前请务必使用CDATA标签将JSON文本串保护起来，`具体参考 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1>`_
    :attach: 附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
    :fee_type: 符合ISO 4217标准的三位字母代码，默认人民币：CNY，其他值列表详见 `货币类型 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_
    :time_start: 订单生成时间，格式为yyyyMMddHHmmss，如2009年12月25日9点10分10秒表示为20091225091010。其他详见 `时间规则 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_
    :time_expire: 订单失效时间，格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010。其他详见 `时间规则 <https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_2>`_ **注意：最短失效时间间隔必须大于5分钟**
    :goods_tag: 商品标记，代金券或立减优惠功能的参数，说明详见 `代金券或立减优惠 <https://pay.weixin.qq.com/wiki/doc/api/tools/sp_coupon.php?chapter=12_1>`_
    :product_id: trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义。
    :limit_pay: 指定不能使用信用卡支付

返回对象
^^^^^^^^^^^^^^^
    :return: Json object

扫码支付
----------

#TODO
