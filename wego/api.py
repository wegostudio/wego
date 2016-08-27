# -*- coding: utf-8 -*-
import random
import hashlib
import wego
import json
import time

class WegoWrapper(object):
    """
    WegoWrpper
    """

    def __init__(self, settings):

        self.settings = settings

    def login_required(self, func):
        """
        修饰器：在需要获取微信用户数据的函数使用
        """
        wechat = wego.wechat.WeChatApi(self.settings)
        wrapper = WegoApi(wechat, func)
        return wrapper.get_wx_user

class WegoApi(object):
    """
    WegoApi
    """

    def __init__(self, wechat, func):
        self.wechat = wechat
        self.settings = wechat.settings
        self.func = func


    def get_wx_user(self, request, *args, **kwargs):

        self.helper = self.settings.HELPER(request)

        if 'code' in self.helper.get_params():
            code = self.helper.get_params().get('code', '')
            openid = self.get_openid(code)
            self.helper.set_session('wx_openid', openid)

        openid = self.helper.get_session('wx_openid')
        if openid:
            self.openid = openid
            request.wego = self
            request.wx_openid = openid

            wx_user = self.get_userinfo()
            if wx_user != 'error':
                request.wx_user = wx_user
                return self.func(request, *args, **kwargs)

        return self.redirect_for_code()

    def redirect_for_code(self):
        """
        引导用户到网页授权页面
        """

        redirect_url = self.helper.get_current_path()
        url = self.wechat.get_code_url(redirect_url)

        return self.helper.redirect(url)

    def get_openid(self, code):
        """
        网页授权页面同意后会带上 code 参数跳转至此
        通过 code 参数可以获取 openid
        """

        data = self.wechat.get_access_token(code)

        self.set_user_tokens(data)

        return data['openid']

    def get_userinfo(self):
        """
        通过 openid 与 global_access_token 获取用户具体信息
        :return: :class:`WeChatUser <wego.wechat.WeChatUser>` object
        """

        if self.settings.USERINFO_EXPIRE:
            wx_userinfo = self.helper.get_session('wx_userinfo')
            if wx_userinfo:
                wx_userinfo = dict({'expires_at': 0} ,**json.loads(wx_userinfo))
                if wx_userinfo['expires_at'] > time.time():
                    return wego.wechat.WeChatUser(self, wx_userinfo)

        if self.helper.get_session('wx_access_token_expires_at') < time.time():
            refresh_token = self.helper.get_session('wx_refresh_token')
            new_token = self.wechat.refresh_access_token(refresh_token)
            if new_token == 'error':
                return 'error'
            self.set_user_tokens(new_token)

        access_token = self.helper.get_session('wx_access_token')
        data = self.wechat.get_userinfo_by_token(self.openid, access_token)
        self.set_userinfo(data)

        return wego.wechat.WeChatUser(self, data)

    def set_userinfo(self, data):
        data['expires_at'] = time.time() + self.settings.USERINFO_EXPIRE
        self.helper.set_session('wx_userinfo', json.dumps(data))

    def set_user_tokens(self, data):

        self.helper.set_session('wx_access_token', data['access_token'])
        self.helper.set_session('wx_access_token_expires_at', time.time() + data['expires_in'] - 180)
        self.helper.set_session('wx_refresh_token', data['refresh_token'])

     
    def get_unifiedorder_info(self, **kwargs):
        """ 
        unifiedorder settings, get wechat config at https://api.mch.weixin.qq.com/pay/unifiedorder

        :param body: BODY is order infos
        :param out_trade_no: (商户订单号)
        :param total_fee: (总金额)
        :param spbill_create_ip: (客户段ip)
        :param notify_url: (通知地址)
        :param trade_type: (交易类型)
        :return: :class:`WegoApi <wego.api.WegoApi>` object
        :rtype: WegoApi
        """
        kwargs['nonce_str'] = _get_random_code()
        return wechat.get_unifiedorder(kwargs)




    def _get_random_code(self, length=6):
        """
        get random code
        """
        return ''.join(random.sample('0123456789', length))


   
