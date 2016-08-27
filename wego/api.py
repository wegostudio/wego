# -*- coding: utf-8 -*-
import random
import hashlib
from exceptions import WegoApiError, WeChatUserError
import wego
import json
import time


class WegoApi(object):
    """
    Wego api dead simple for humans.
    """

    def __init__(self, settings):

        self.settings = settings
        self.wechat = wego.WeChatApi(settings)

    def login_required(self, func):
        """
        Decorator：use for request function, and it will init an independent WegoApi instance.
        """

        def get_wx_user(request, *args, **kwargs):
            """
            Called by login_required, it will set some attributes to function`s first param.

            :param request: Function`s first param.
            :return: Subject to availability.
            """

            helper = self.settings.HELPER(request)

            code = helper.get_params().get('code', '')
            if code:
                openid = self.get_openid(code)
                helper.set_session('wx_openid', openid)

            openid = helper.get_session('wx_openid')
            if openid:
                self.openid = openid
                request.wego = self
                request.wx_openid = openid

                wx_user = self.get_userinfo(helper)
                if wx_user != 'error':
                    request.wx_user = wx_user
                    return func(request, *args, **kwargs)

            return self.redirect_for_code(helper)

        return get_wx_user

    def redirect_for_code(self, helper):
        """
        Let user jump to wechat authorization page.

        :return: Redirect object
        """

        redirect_url = helper.get_current_path()
        url = self.wechat.get_code_url(redirect_url)

        return helper.redirect(url)

    def get_openid(self, code):
        """
        Get user openid.

        :param code: A code that user redirect back will bring.
        :return: openid
        """

        data = self.wechat.get_access_token(code)

        self._set_user_tokens(helper, data)

        return data['openid']

    def get_userinfo(self, helper):
        """
        Get user info.

        :return: :class:`WeChatUser <wego.api.WeChatUser>` object
        """

        wechat_user = self._get_userinfo_from_session(helper)
        if wechat_user:
            return wechat_user

        if helper.get_session('wx_access_token_expires_at') < time.time():
            refresh_token = helper.get_session('wx_refresh_token')
            new_token = self.wechat.refresh_access_token(refresh_token)
            if new_token == 'error':
                return 'error'
            self._set_user_tokens(helper, new_token)

        access_token = helper.get_session('wx_access_token')
        data = self.wechat.get_userinfo_by_token(self.openid, access_token)
        self._set_userinfo_to_session(helper,data)

        return WeChatUser(self, data)

    def _get_userinfo_from_session(self, helper):
        """
        Get user info from session.

        :return: None or :class:`WeChatUser <wego.api.WeChatUser>` object
        """

        if self.settings.USERINFO_EXPIRE:
            wx_userinfo = helper.get_session('wx_userinfo')
            if wx_userinfo:
                wx_userinfo = dict({'expires_at': 0}, **json.loads(wx_userinfo))
                if wx_userinfo['expires_at'] > time.time():
                    return WeChatUser(self, wx_userinfo)
        return None

    def _set_userinfo_to_session(self, helper, data):
        """
        Set user info into session.

        :param data: user info.
        :return: None
        """

        data['expires_at'] = time.time() + self.settings.USERINFO_EXPIRE
        helper.set_session('wx_userinfo', json.dumps(data))

    def _set_user_tokens(self, helper, data):
        """
        Set user all tokens to sessions.

        :param data: Tokens.
        :return: None
        """

        helper.set_session('wx_access_token', data['access_token'])
        helper.set_session('wx_access_token_expires_at', time.time() + data['expires_in'] - 180)
        helper.set_session('wx_refresh_token', data['refresh_token'])

    def get_unifiedorder_info(self, **kwargs):
        """ 
        unifiedorder settings, get wechat config at https://api.mch.weixin.qq.com/pay/unifiedorder
        You can take return value as wechat api onBridgeReady's parameters directly

        You don't need to include appid, mch_id, nonce_str, sign, openid
        because these four parameters set by WeChatApi,
        but the following parameters are necessary, you must be included in the kwargs
        and you must follow the format below as the parameters's key

        :param body: Goods are simply described, the field must be in strict accordance with the
         specification, specific see parameters

        :param out_trade_no: Merchants system internal order number, within 32 characters,
         can include letters, other see merchant order number

        :param total_fee: Total amount of orders, the unit for points, as shown in the payment amount

        :param spbill_create_ip: APP and web payment submitted to client IP, Native fill call
         WeChat payment API machine IP.

        :param notify_url: Receive pay WeChat asynchronous notification callback address,
         notify the url must be accessible url directly, cannot carry parameters.

        :param trade_type: Values are as follows: the JSAPI, NATIVE APP, details see parameter regulation

        :return: {'appId': string,
                'timeStamp': value,
                'nonceStr': value,
                'package': value,
                'signType': value,
                'paySign': value,}
        """

        # invoking get_unifiedorder to obtain the return value
        kwargs['openid'] = self.openid
        order_info = self.wechat.get_unifiedorder(kwargs)

        # packaged in a dict
        data = dict()
        data['appId'] = order_info['appid']
        data['timeStamp'] = str(int(time.time()))
        data['nonceStr'] = order_info['nonce_str']
        data['package'] = 'prepay_id=' + order_info['prepay_id']
        data['signType'] = 'MD5'
        data['paySign'] = self.wechat._make_sign(data)

        return data     





   
    def create_group(self, name):
        """
        Create a new group.

        :param name: Group name.
        :return: :dict: {'id': 'int', 'name':'str'}
        """

        return self.wechat.create_group(name)['group']

    def get_groups(self):
        """
        Get all groups.

        :return: :dict: {'your_group_id': {'name':'str', 'count':'int'}}
        """

        data = self.wechat.get_all_groups()
        return {i.pop('id'): i for i in data['groups']}

    def _get_groupid(self, group):
        """
        Input group id or group name and return group id.

        :param group: Group name or group id.
        :return: group id
        """

        groups = self.get_groups()
        if type(group) is int:
            groupid = int(group)
        else:
            group = str(group)
            for i in groups:
                if groups[i]['name'] == group:
                    groupid = i
                    break
            else:
                raise WegoApiError(u'Without this group(没有这个群组)')

        if not groups.has_key(groupid):
            raise WegoApiError(u'Without this group(没有这个群组)')

        return groupid

    def change_group_name(self, group, name):
        """
        Change group name.

        :param group: Group id or group name.
        :param name: New group name
        :return: :Bool
        """

        groupid = self._get_groupid(group)
        data = self.wechat.change_group_name(groupid, name)
        return not data['errcode']
    
    def change_user_group(self, group):
        """
        Change user group.

        :param group: Group id or group name.
        :return: :Bool .
        """

        groupid = self._get_groupid(group)
        data = self.wechat.change_user_group(self.openid, groupid)
        return not data['errcode']

    def del_group(self, group):
        """
        Delete group.

        :param group: Group id or group name.
        :return: :Bool
        """

        groupid = self._get_groupid(group)
        data = self.wechat.del_group(groupid)
        return not data['errcode']

    def create_menu(self, *args):
        """
        Create menu by wego.button

        :return: :Bool
        """

        data = {
            'button': [i.json for i in args]
        }
 
        data = self.wechat.create_menu(data)

        return not data['errcode']

class WeChatUser(object):
    """
    A lazy and smart wechat user object. You can set user remark, group, groupid direct,
    because of group name can be repeated, so if you set the group by group name, it may not be accurate.
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
                        break
                else:
                    raise WeChatUserError(u'Without this group(没有这个群组)')

            groupid = value 
            if not groups.has_key(groupid):
                raise WeChatUserError(u'Without this group(没有这个群组)')

            self.wego.change_user_group(groupid)
        
        super(WeChatUser, self).__setattr__(key, value)

    def get_ext_userinfo(self):
        """
        Get user extra info, such as subscribe, language, remark and groupid.

        :return: :dict: User data
        """

        self.data['remark'] = ''
        self.data['groupid'] = ''

        data = self.wego.wechat.get_userinfo(self.wego.openid)
        self.data = dict(self.data, **data)
        self.is_upgrade = True

        return self.data


# TODO 更方便定制
def official_get_global_access_token(self):
    """
    Get global access token.

    :param self: Call self.get_global_access_token() for get global access token.
    :return: :str: Global access token
    """

    if not self.global_access_token or self.global_access_token['expires_in'] <= int(time.time()):
        self.global_access_token = self.get_global_access_token()
        self.global_access_token['expires_in'] += int(time.time()) - 180

    return self.global_access_token['access_token']

