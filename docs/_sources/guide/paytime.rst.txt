.. _paytime:

微信支付
==========

微信的支付方式有多种，目前 wego 只实现了公众号支付，其他支付方式正在开发中...


准备工作
--------

初始化生成 w 实例时，请记得将所需参数填入，详细参数请看 :ref:`pay_options`


公众号支付
----------

在 wego，你只需要填入对应的参数即可生成前端调起微信支付所需的 json 数据，下面是一个访问便立即调起微信支付的示例。

::

    @w.login_required
    def wechat_pay(request):
        import time
        order = 'ordernum' + str(int(time.time()))
        raw_html = template % json.dumps(w.unified_order(
            openid=request.wx_openid,
            body='test',
            out_trade_no= order,
            total_fee='1',
            spbill_create_ip='113.16.139.82',
            trade_type='JSAPI',
        ))

        return HttpResponse(raw_html)


    template = '''<script>
    function onBridgeReady(){
      WeixinJSBridge.invoke(
        'getBrandWCPayRequest', %s,
        function(res){
          if(res.err_msg == "get_brand_wcpay_request：ok" ) {
            alert('支付成功!')
          }
        }
      );
    }
    if (typeof WeixinJSBridge == "undefined"){
      if( document.addEventListener ){
        document.addEventListener('WeixinJSBridgeReady', onBridgeReady, false);
      }else if (document.attachEvent){
        document.attachEvent('WeixinJSBridgeReady', onBridgeReady);
        document.attachEvent('onWeixinJSBridgeReady', onBridgeReady);
      }
    }else{
      onBridgeReady();
    }
    </script>'''