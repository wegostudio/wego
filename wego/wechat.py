# -*- coding: utf-8 -*-
from exceptions import WechatApiError
import requests
import random
import re
import hashlib
import time

# TODO 返回数据 sign 验证


class WechatApi(object):
    """
    Wechat Api
    """

    def __init__(self, settings):

        self.settings = settings
        self.global_access_token = {}

        # TODO for loop
        self.wego_get_current_path = settings['HELPER'].wego_get_current_path
        self.wego_get_params = settings['HELPER'].wego_get_params
        self.wego_set_session = settings['HELPER'].wego_set_session
        self.wego_get_session = settings['HELPER'].wego_get_session
        self.wego_redirect = settings['HELPER'].wego_redirect

    def login_required(self, func):
        """
        修饰器：在需要获取微信用户数据的函数使用
        """

        def wrapper(request, *args, **kv):

            if 'code' in request.wego_get_params():
                request.get_openid(self.wego_get_params(request)['code'])

            openid = self.wego_set_session('openid')
            if openid:
                request.openid = openid
                request.wx_user = self.get_userinfo()
                return func(self, *args, **kv)
            else:
                return self.get_code(self.wego_get_current_path())

        return wrapper

    def get_code(self, redirect_url=None, state='STATE'):
        """
        引导用户到网页授权页面
        """

        if not redirect_url:
            redirect_url = self.settings['REDIRECT_URL']

        url = ('https://open.weixin.qq.com/connect/oauth2/authorize?' +
               'appid=%s&redirect_uri=%s' +
               '&response_type=code' +
               '&scope=snsapi_userinfo' +
               '&state=%s#wechat_redirect') % (self.settings['APP_ID'], redirect_url, state)

        return self.wego_redirect(url)

    def get_openid(self, code):
        """
        网页授权页面同意后会带上 code 参数跳转至此
        通过 code 参数可以获取 openid
        """

        # 以下是微信网页授权后的回调处理
        # 获取 openid 和 access_token
        data = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params={
            'appid': self.settings['APP_ID'],
            'secret': self.settings['APP_SECRET'],
            'code': code,
            'grant_type': 'authorization_code'
        }).json()

        access_token = data['access_token']
        refresh_token = data['refresh_token']

        self.wego_set_session['openid'] = data['openid']

    def get_userinfo(self, openid):
        """
        通过 openid 与 global_access_token 获取用户具体信息
        :return: :class:`WechatUser <wego.wechat.WechatUser>` object
        """

        access_token = self.settings['GET_ACCESS_TOKEN'](self)
        data = {
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }
        data = requests.get('https://api.weixin.qq.com/cgi-bin/user/info', params=data).json()
        if 'errcode' in data.keys():
            raise WechatApiError('errcode: {}, msg: {}'.format(data['errcode'], data['errmsg']))

        return data
#
#
# def refresh_userinfo(openid, request):
#     """
#     通过保存在数据库内 openid 对应的 refresh_token 刷新用户信息
#     """
#
#     #  刷新用户信息
#     try:
#         wx_user = WX_User.objects.get(openid=openid)
#     except:
#         #  当做 refresh_token 过期处理，可能是之前没有获取到完整数据，强制重新授权
#         print 'request.session.flush() except ' + openid
#         return request.session.flush()
#
#     refresh_token = wx_user.refresh_token
#     new_token = requests.get('https://api.weixin.qq.com/sns/oauth2/refresh_token', params={
#         'appid': AppID,
#         'grant_type': 'refresh_token',
#         'refresh_token': refresh_token
#     }).json()
#
#     if 'errmsg' in new_token.keys():
#         # refresh_token 过期
#         print 'equest.session.flush() errmg ' + openid
#         return request.session.flush()
#
#     access_token = new_token['access_token']
#     refresh_token = new_token['refresh_token']
#     return get_userinfo(openid, access_token, refresh_token)
#
#
# def set_userinfo(data):
#     """
#     保存用户信息至数据库
#     """
#
#     openid = data['openid']
#
#     # TODO  判断是否存在该用户了，存在就 update
#     wx_user = WX_User.objects.filter(openid=openid)
#     if len(wx_user):
#         wx_user = wx_user[0]
#         wx_user.nickname = data['nickname']
#         wx_user.sex = data['sex']
#         wx_user.province = data['province']
#         wx_user.city = data['city']
#         wx_user.country = data['country']
#         wx_user.headimgurl = data['headimgurl']
#         wx_user.privilege = data['privilege']
#         wx_user.refresh_token = data['refresh_token']
#         wx_user.save()
#
#     else:
#         WX_User.objects.create(
#             openid=data['openid'],
#             nickname=data['nickname'],
#             sex=data['sex'],
#             province=data['province'],
#             city=data['city'],
#             country=data['country'],
#             headimgurl=data['headimgurl'],
#             privilege=data['privilege'],
#             refresh_token=data['refresh_token'],
#         )
#
#     return openid
#
#
# # 下面是微信支付
#
#
# def make_xml(k, v=None):
#     """
#     递归生成 xml
#     """
#
#     if not v:
#         v = k
#         k = 'xml'
#
#     if type(v) is dict:
#         v = ''.join([make_xml(key, val) for key, val in v.iteritems()])
#     return '<%s>%s</%s>' % (k, v, k)
#
#
# def make_sign(data):
#     """
#     生成微信支付签名
#     """
#     temp = ['%s=%s' % (k, data[k]) for k in sorted(data.keys())]
#     temp.append('key=' + MchSecret)
#     temp = '&'.join(temp)
#
#     md5 = hashlib.md5()
#     md5.update(temp.encode('utf-8'))
#     return md5.hexdigest().upper()
#
#
# def analysis_xml(xml):
#     """
#     将 xml 转成 dict
#     """
#     return {k: v for v, k in re.findall('\<.*?\>\<\!\[CDATA\[(.*?)\]\]\>\<\/(.*?)\>', xml)}
#
#
# def unifiedorder(body, nonce_str, openid, out_trade_no, spbill_create_ip, total_fee, **kv):
#     """
#     https://pay.weixin.qq.com/wiki/doc/api/jsapi.php
#     生成预支付交易订单
#     body: 商品或支付单简要描述
#     nonce_str: 随机字符串，不长于32位。
#     out_trade_no: 商户系统内部的订单号,32个字符内、可包含字母
#     spbill_create_ip: 用户IP
#     支持非必填参数(attach=u'这样传入')
#     """
#
#     data = {
#         'appid': AppID,
#         'body': body,
#         'mch_id': MchId,
#         'nonce_str': nonce_str,
#         'notify_url': WechatNotifyUrl,
#         'openid': openid,
#         'out_trade_no': out_trade_no,
#         'spbill_create_ip': spbill_create_ip,
#         'total_fee': 1 if TEST_MODE else int(total_fee),
#         'trade_type': 'JSAPI'
#     }
#     data = dict(data, **kv)
#
#     data['sign'] = make_sign(data)
#
#     xml = make_xml(data).encode('utf-8')
#     data = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml).content
#     return analysis_xml(data)
#
#
# wechat_notify_signal = django.dispatch.Signal(providing_args=["data"])
#
#
# @csrf_exempt
# def wechat_notify(request):
#     if request.method == 'POST':
#         data = analysis_xml(request.body)
#         wechat_notify_signal.send(sender='wechat.py', data=data)
#         return HttpResponse(make_xml({
#             'return_code': 'SUCCESS',
#             'return_msg': 'OK'
#         }))
#
#     return HttpResponse(make_xml({
#         'return_code': 'FAIL',
#         'return_msg': 'ERROR'
#     }))
#
#
# def get_spread_brcode(scene_str):
#     data = {
#         'action_name': 'QR_LIMIT_STR_SCENE',
#         'action_info': {
#             'scene': {
#                 'scene_str': scene_str
#             }
#         }
#     }
#     access_token = get_token()
#     url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
#
#     rep = requests.post(url, data=json.dumps(data))
#     return rep.json()
#
#
# def wx_info(openid):
#     access_token = get_token()
#     data = {
#         'access_token': access_token,
#         'openid': openid,
#         'lang': 'zh_CN'
#     }
#
#     url = 'https://api.weixin.qq.com/cgi-bin/user/info'
#     rep = requests.get(url, params=data)
#
#     wx_info = rep.json()
#
#     return wx_info
#

# 以下事件都在 spread 中处理
# wechat_qr_notify_signal = django.dispatch.Signal(providing_args=["data"])
# wechat_msg_notify_signal = django.dispatch.Signal(providing_args=["data"])
# wechat_subscribe_notify_signal = django.dispatch.Signal(providing_args=["data"])
#
#
# @csrf_exempt
# def wechat_event_notify(request):
#     if request.method == 'POST':
#         data = analysis_xml(request.body)
#         if 'Ticket' in data.keys():
#             wechat_qr_notify_signal.send(sender='wechat.py', data=data)
#         elif data['MsgType'] == 'text':
#             signal_return = wechat_msg_notify_signal.send(sender='wechat.py', data=data)
#             return HttpResponse(make_xml(signal_return[0][1]))
#         else:
#             print data
#
#         if data['MsgType'] == 'event':
#             if data['Event'] == 'subscribe':
#                 signal_return = wechat_subscribe_notify_signal.send(sender='wechat.py', data=data)
#                 return HttpResponse(make_xml(signal_return[0][1]))
#
#         return HttpResponse('')
#
#     return HttpResponse('')
#
#
# def get_random_code(length=6):
#     """随机数"""
#     return "".join(random.sample('0123456789', length))
