# -*- coding: utf-8 -*-
from exceptions import WegoApiError
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
        self.wego_api = WegoApi(wechat, func)
        return self.wego_api.get_wx_user

    def __getattr__(self, key):
        if hasattr(self.wego_api, key):
            return getattr(self.wego_api, key)

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
        :return: :class:`WeChatUser <wego.api.WeChatUser>` object
        """

        if self.settings.USERINFO_EXPIRE:
            wx_userinfo = self.helper.get_session('wx_userinfo')
            if wx_userinfo:
                wx_userinfo = dict({'expires_at': 0} ,**json.loads(wx_userinfo))
                if wx_userinfo['expires_at'] > time.time():
                    return WeChatUser(self, wx_userinfo)

        if self.helper.get_session('wx_access_token_expires_at') < time.time():
            refresh_token = self.helper.get_session('wx_refresh_token')
            new_token = self.wechat.refresh_access_token(refresh_token)
            if new_token == 'error':
                return 'error'
            self.set_user_tokens(new_token)

        access_token = self.helper.get_session('wx_access_token')
        data = self.wechat.get_userinfo_by_token(self.openid, access_token)
        self.set_userinfo(data)

        return WeChatUser(self, data)

    def set_userinfo(self, data):
        data['expires_at'] = time.time() + self.settings.USERINFO_EXPIRE
        self.helper.set_session('wx_userinfo', json.dumps(data))

    def set_user_tokens(self, data):

        self.helper.set_session('wx_access_token', data['access_token'])
        self.helper.set_session('wx_access_token_expires_at', time.time() + data['expires_in'] - 180)
        self.helper.set_session('wx_refresh_token', data['refresh_token'])

    def create_group(self, name):
        """
        :return: :dict: {'id': 'int', 'name':'str'}
        """

        return self.wechat.create_group(name)['group']


    def get_groups(self):
        """
        :return: :dict: {'your_group_id': {'name':'str', 'count':'int'}}
        """

        data = self.wechat.get_all_groups()
        return {i.pop('id'): i for i in data['groups']}

    def _get_groupid(self, group):
        """
        int 类型会当成 id，str 类型会当成 name
        """

        groups = self.get_groups()
        if type(group) is int:
            groupid = int(group)
        else:
            group = str(group)
            for i in groups:
                if groups[i]['name'] == group:
                    groupid = i
                    break;
            else:
                raise WegoApiError(u'Without this group(没有这个群组)')

        if not groups.has_key(groupid):
            raise WegoApiError(u'Without this group(没有这个群组)')

        return groupid

    def change_group_name(self, group, name):

        groupid = self._get_groupid(group)
        data = self.wechat.change_group_name(groupid, name)
        return not data['errcode']
    
    def change_user_group(self, group):

        groupid = self._get_groupid(group)
        data = self.wechat.change_user_group(self.openid, groupid)
        return not data['errcode']

    def del_group(self, group):

        groupid = self._get_groupid(group)
        data = self.wechat.del_group(groupid)
        return not data['errcode']


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


# TODO 更方便定制
def official_get_global_access_token(self):
    """
    获取全局 access token
    """

    if not self.global_access_token or self.global_access_token['expires_in'] <= int(time.time()):
        self.global_access_token = self.get_global_access_token()
        self.global_access_token['expires_in'] += int(time.time()) - 180

    return self.global_access_token['access_token']

