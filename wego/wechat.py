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

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
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

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
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

    def get_global_access_token(self):

        data = requests.get("https://api.weixin.qq.com/cgi-bin/token", params={
            'grant_type': 'client_credential',
            'appid': self.settings.APP_ID,
            'secret': self.settings.APP_SECRET
        }).json()

        return data

    def create_group(self, name):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'group': {
                'name': name
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/groups/create?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def get_all_groups(self):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        url = "https://api.weixin.qq.com/cgi-bin/groups/get?access_token=%s" % access_token
        req = requests.get(url)

        return req.json()

    def change_group_name(self, groupid, name):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'group': {
                'id': groupid,
                'name': name
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/groups/update?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def change_user_group(self, openid, groupid):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'openid': openid,
            'to_groupid': groupid
        }
        url = 'https://api.weixin.qq.com/cgi-bin/groups/members/update?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def del_group(self, groupid):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'group': {
                'id': groupid
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/groups/delete?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data




# TODO 更方便定制
def official_get_global_access_token(self):
    """
    获取全局 access token
    """

    if not self.global_access_token or self.global_access_token['expires_in'] <= int(time.time()):
        self.global_access_token = self.get_global_access_token()
        self.global_access_token['expires_in'] += int(time.time()) - 180

    return self.global_access_token['access_token']


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

        if key == 'group' and not self.data.has_key(key):
            self.data['group'] = self.wego.get_groups()[self.groupid]

        if self.data.has_key(key):
            return self.data[key]
        return ''

    def __setattr__(self, key, value):
        """
        支持直接设置 remark 和 group，group 通过名称设置用户组，将匹配第一个同名的组，通过 groupid 设置会更准确。
        """
        
        if key == 'remark':
            if self.subscribe != 1:
                raise WeChatUserError('The user does not subscribe you')

            if self.data['remark'] != value:
                self.wego.wechat.set_user_remark(self.wego.openid, value)
                self.data[key] = value

        if key in ['group', 'groupid']:
            groups = self.wego.get_groups()
            if key == 'group':
                for i in groups:
                    if groups[i]['name'] == value:
                        value = i
                        break;
                else:
                    raise WeChatUserError(u'Without this group(没有这个群组)')

            groupid = value 
            if not groups.has_key(groupid):
                raise WeChatUserError(u'Without this group(没有这个群组)')

            self.wego.change_user_group(groupid)
        
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

        return self.data

