# -*- coding: utf-8 -*-
from exceptions import WeChatApiError, WeChatUserError
from urllib import quote
import requests
import random
import re
import hashlib
import json
import time


class WeChatApi(object):
    """
    WeChat Api
    """

    def __init__(self, settings):

        self.settings = settings
        self.global_access_token = {}

    def get_code_url(self, redirect_url, state='STATE'):

        if redirect_url:
            redirect_url = quote(self.settings.REGISTER_URL + redirect_url[1:])
        else:
            redirect_url = self.settings.REDIRECT_URL

        url = ('https://open.weixin.qq.com/connect/oauth2/authorize?' +
               'appid=%s&redirect_uri=%s' +
               '&response_type=code' +
               '&scope=snsapi_userinfo' +
               '&state=%s#wechat_redirect') % (self.settings.APP_ID, redirect_url, state)

        return url

    def get_access_token(self, code):

        data = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params={
            'appid': self.settings.APP_ID,
            'secret': self.settings.APP_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }).json()

        return data

    def refresh_access_token(self, refresh_token):
        token = requests.get('https://api.weixin.qq.com/sns/oauth2/refresh_token', params={
            'appid': self.settings.APP_ID,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }).json()

        if 'errcode' in token.keys():
            return 'error'

        return token

    def get_userinfo(self, openid):

        access_token = self.settings.GET_ACCESS_TOKEN(self)
        data = {
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'
        }
        data = requests.get('https://api.weixin.qq.com/cgi-bin/user/info', params=data).json()

        if 'errcode' in data.keys():
            raise WeChatApiError('errcode: {}, msg: {}'.format(data['errcode'], data['errmsg']))

        return data

    def set_user_remark(self, openid, remark):

        access_token = self.settings.GET_ACCESS_TOKEN(self)
        data = {
            'openid': openid,
            'remark': remark
        }
        url = 'https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        if 'errcode' in data.keys() and data['errcode'] != 0:
            raise WeChatApiError('errcode: {}, msg: {}'.format(data['errcode'], data['errmsg']))

    def get_userinfo_by_token(self, openid, access_token):

        data = requests.get('https://api.weixin.qq.com/sns/userinfo', params={
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'
        })

        data.encoding = 'utf-8'
        return data.json()


class WeChatUser(object):
    """
    WeChat user https://mp.weixin.qq.com/wiki/1/8a5ce6257f1d3b2afb20f83e72b72ce9.html
    """

    def __init__(self, wego, data):
        
        self.wego = wego
        self.data = data
        self.is_upgrade = False

    def __getattr__(self, key):
        

        ext_userinfo = ['subscribe', 'language', 'remark', 'groupid']
        if key in ext_userinfo and not self.is_upgrade:
            self.get_ext_userinfo()

        return self.data[key]

    def __setattr__(self, key, value):
        
        if key == 'remark':
            if self.subscribe != 1:
                raise WeChatUserError('The user does not subscribe you')

            if self.data['remark'] != value:
                self.wego.wechat.set_user_remark(self.wego.openid, value)
                self.data[key] = value
        
        super(WeChatUser, self).__setattr__(key, value)

    def get_ext_userinfo(self):
        """
        groupid subscribe language remark
        """

        self.data['remark'] = ''
        self.data['groupid'] = ''

        data = self.wego.wechat.get_userinfo(self.wego.openid)
        self.data = dict(self.data, **data)
        self.is_upgrade = True

