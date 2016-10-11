.. _pay:

微信支付
==========

微信的支付方式有多种，目前 wego 只实现了公众号支付、扫码支付，其他支付方式正在开发中...


准备工作
--------

初始化生成 w 实例时，请记得将所需参数填入，详细参数请看 :ref:`pay_options`


公众号支付
----------

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
    :openid:
    :body:
    :out_trade_no:
    :total_fee:
    :trade_type:
    :spbill_create_ip:

可选参数说明
^^^^^^^^^^^^^^^
    :device_data:
    :detail:
    :attach:
    :fee_type:
    :time_start:
    :time_expire:
    :goods_tag:
    :product_id:
    :limit_pay:

返回对象
^^^^^^^^^^^^^^^
    :return: Json object

扫码支付
----------

#TODO