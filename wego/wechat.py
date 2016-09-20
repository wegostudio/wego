# -*- coding: utf-8 -*-
from .exceptions import WeChatApiError, WeChatUserError
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
import requests
import hashlib
import json
import re


class WeChatApi(object):
    """
    WeChat Api just do one thing: give params to wechat and get the data what wechat return.
    """

    def __init__(self, settings):

        self.settings = settings
        self.global_access_token = {}

    def get_code_url(self, redirect_url, state='STATE'):
        """
        Get the url which 302 jump back and bring a code.

        :param redirect_url: Jump back url
        :param state: Jump back state
        :return: url
        """

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
        """
        Use code for get access token, refresh token, openid etc.

        :param code: A code see function get_code_url.
        :return: Raw data that wechat returns.
        """

        data = requests.get('https://api.weixin.qq.com/sns/oauth2/access_token', params={
            'appid': self.settings.APP_ID,
            'secret': self.settings.APP_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }).json()

        return data

    def refresh_access_token(self, refresh_token):
        """
        Refresh user access token by refresh token.

        :param refresh_token: function get_access_token returns.
        :return: Raw data that wechat returns.
        """

        data = requests.get('https://api.weixin.qq.com/sns/oauth2/refresh_token', params={
            'appid': self.settings.APP_ID,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }).json()

        if 'errcode' in data.keys():
            return 'error'

        return data

    def get_userinfo(self, openid):
        """
        Get user info with global access token (content subscribe, language, remark and groupid).

        :param openid: User openid.
        :return: Raw data that wechat returns.
        """

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
        """
        Set user remark.

        :param openid: User openid.
        :param remark: The remark you want to set.
        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'openid': openid,
            'remark': remark
        }
        url = 'https://api.weixin.qq.com/cgi-bin/user/info/updateremark?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        if 'errcode' in data.keys() and data['errcode'] != 0:
            raise WeChatApiError('errcode: {}, msg: {}'.format(data['errcode'], data['errmsg']))

    def is_access_token_has_expired(sele, openid, access_token):
        """
        Determine whether the user access token has expired
 
        :param openid: User openid.
        :param access_token: function get_access_token returns.
        :return: Raw data that wechat returns.
        """

        data = {
            'access_token': access_token,
            'openid': openid,
        }
        url = 'https://api.weixin.qq.com/sns/auth'
        data = requests.post(url, params=data).json()

        return data

    def get_userinfo_by_token(self, openid, access_token):
        """
        Get user info with user access token (without subscribe, language, remark and groupid).

        :param openid: User openid.
        :param access_token: function get_access_token returns.
        :return: Raw data that wechat returns.
        """

        data = requests.get('https://api.weixin.qq.com/sns/userinfo', params={
            'access_token': access_token,
            'openid': openid,
            'lang': 'zh_CN'
        })

        data.encoding = 'utf-8'
        return data.json()

    def get_global_access_token(self):
        """
        Get global access token.

        :return: Raw data that wechat returns.
        """

        data = requests.get("https://api.weixin.qq.com/cgi-bin/token", params={
            'grant_type': 'client_credential',
            'appid': self.settings.APP_ID,
            'secret': self.settings.APP_SECRET
        }).json()

        return data

    @staticmethod
    def _make_xml(k, v=None):
        """
        Recursive generate XML
        """

        if not v:
            v = k
            k = 'xml'
        if type(v) is dict:
            v = ''.join([WeChatApi._make_xml(key, val) for key, val in v.iteritems()])
        elif type(v) is list:
            l = len(k)+2
            v = ''.join([WeChatApi._make_xml(k, val) for val in v])[l:(l+1)*-1]
        elif type(v) in [str, unicode]:
            return '<%s><![CDATA[%s]]></%s>' % (k, v, k)
        return '<%s>%s</%s>' % (k, v, k)

    def _analysis_xml(self, xml):
        """
        Convert the XML to dict
        """

        if not xml:
            return {}
        return {k: v for v,k in re.findall('\<.*?\>\<\!\[CDATA\[(.*?)\]\]\>\<\/(.*?)\>', xml)}

    def get_unifiedorder(self, data):

        xml = self._make_xml(data).encode('utf-8')
        data = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml).content

        return self._analysis_xml(data)

    def get_orderquery(self, data):
        """
        Get order query.

        :return: Raw data that wechat returns.
        """

        xml = self._make_xml(data).encode('utf-8')
        data = requests.post('https://api.mch.weixin.qq.com/pay/orderquery', data=xml).content

        return self._analysis_xml(data)

    def close_order(self, data):
        """
        Get close_order info.

        :return: Raw data that wechat returns.
        """

        xml = self._make_xml(data).encode('utf-8')
        data = requests.post('https://api.mch.weixin.qq.com/pay/closeorder', data=xml).content

        return self._analysis_xml(data)

    def refund(self, data):
        """
        refund.

        :return: Raw data that wechat returns.
        """
        xml = self._make_xml(data).encode('utf-8')
        data = requests.post('https://api.mch.weixin.qq.com/secapi/pay/refund', data=xml).content
        return self._analysis_xml(data)

    def refund_query(self, data):
        """
        refund query

        :return: Raw data that wechat returns.
        """
        xml = self._make_xml(data).encode('utf-8')
        data = requests.post('https://api.mch.weixin.qq.com/pay/refundquery', data=xml).content
        return self._analysis_xml(data)

    def download_bill(self, data):
        """
        download bill

        :return: Raw data that wechat returns.
        """
        xml = self._make_xml(data).encode('utf-8')
        data = requests.post('https://api.mch.weixin.qq.com/pay/downloadbill', data=xml).content
        return self._analysis_xml(data)

    def report(self, data):
        """
        report

        :return: Raw data that wechat returns.
        """
        data = requests.post('https://api.mch.weixin.qq.com/payitil/report', data=xml).content
        return self._analysis_xml(data)

    def create_group(self, name):
        """
        Create a user group.

        :param name: Group name.
        :return: Raw data that wechat returns.
        """

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
        """
        Get all user groups.

        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        url = "https://api.weixin.qq.com/cgi-bin/groups/get?access_token=%s" % access_token
        req = requests.get(url)

        return req.json()

    def get_user_groups(self, openid):
        """
        Get all a user groups.

        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'openid': openid
        }
        url = "https://api.weixin.qq.com/cgi-bin/groups/getid?access_token=%s" % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def change_group_name(self, groupid, name):
        """
        Change group name.

        :param groupid: Group ID.
        :param name: New name.
        :return: Raw data that wechat returns.
        """

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
        """
        Move user to a new group.

        :param openid: User openid.
        :param groupid: Group ID.
        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'openid': openid,
            'to_groupid': groupid
        }
        url = 'https://api.weixin.qq.com/cgi-bin/groups/members/update?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def del_group(self, groupid):
        """
        Delete a group.

        :param groupid: Group id.
        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'group': {
                'id': groupid
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/groups/delete?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def create_menu(self, data):
        """
        Create a menu.

        :param data: Menu data.
        :return: Raw data that wechat returns.
        """
        
        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % access_token
        data = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8')).json()

        return data

    def create_conditional_menu(self, data):
        """
        Create a conditional menu.

        :param data: Menu data.
        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        url = "https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token=%s" % access_token
        data = requests.post(url, data=json.dumps(data, ensure_ascii=False).encode('utf8')).json()

        return data

    def get_menus(self):
        """
        Get all menus.

        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        url = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % access_token
        data = requests.get(url).json()

        return data

    def del_all_menus(self):
        """
        Delete all menus, contain conditional menu.

        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % access_token
        data = requests.get(url).json()

        return data

    def del_conditional_menu(self, menu_id):
        """
        Delete conditional menus, contain conditional menu.

        :return: Raw data that wechat returns.
        """

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'menuid': menu_id
        }
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delconditional?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data







    def add_material(self, **kwargs):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            "articles": [{
                    "title": kwargs['title'],
                    "thumb_media_id": kwargs['thumb_media_id'],
                    "author": kwargs['author'],
                    "digest": kwargs['digest'],
                    "show_cover_pic": kwargs['show_cover_pic'],
                    "content": kwargs['content'],
                    "content_source_url": kwargs['content_source_url']
                },
            ]
        }

        url = 'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def get_material(self, media_id):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            "media_id": media_id,
        }

        url = 'https://api.weixin.qq.com/cgi-bin/material/get_material?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def delete_material(self, media_id):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            "media_id": media_id,
        }

        url = 'https://api.weixin.qq.com/cgi-bin/material/del_material?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def update_material(self, **kwargs):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'media_id': kwargs['media_id'],
            'index': kwargs['index'],
            'articles': {
                'title': kwargs['title'],
                'thumb_media_id': kwargs['thumb_media_id'],
                'author': kwargs['author'],
                'digest': kwargs['digest'],
                'show_cover_pic': kwargs['show_cover_pic'],
                'content': kwargs['content'],
                'content_source_url': kwargs['content_source_url']
            }
        }

        url = 'https://api.weixin.qq.com/cgi-bin/material/update_news?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def get_materials_count(self):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)

        url = 'https://api.weixin.qq.com/cgi-bin/material/get_materialcount?access_token=%s' % access_token
        data = requests.get(url).json()

        return data

    def get_materials_list(self, material_type, offset, count):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            "type": material_type,
            "offset": offset,
            "count": count
        }

        url = 'https://api.weixin.qq.com/cgi-bin/material/batchget_material?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def create_scene_qrcode(self, scene_id, expire):
        
        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'expire_seconds': expire, 
            'action_name': 'QR_SCENE', 
            'action_info': {
                'scene': {
                    'scene_id': scene_id
                }
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def create_limit_scene_qrcode(self, scene_id):
        
        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'action_name': 'QR_LIMIT_SCENE', 
            'action_info': {
                'scene': {
                    'scene_id': scene_id
                }
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def create_limit_str_scene_qrcode(self, scene_str):
        
        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'action_name': 'QR_LIMIT_SCENE', 
            'action_info': {
                'scene': {
                    'scene_str': scene_str
                }
            }
        }
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

    def create_short_url(self, url):

        access_token = self.settings.GET_GLOBAL_ACCESS_TOKEN(self)
        data = {
            'action': 'long2short',
            'long_url': url
        }
        url = 'https://api.weixin.qq.com/cgi-bin/shorturl?access_token=%s' % access_token
        data = requests.post(url, data=json.dumps(data)).json()

        return data

