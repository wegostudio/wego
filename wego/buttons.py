# -*- coding: utf-8 -*-
from wego.exceptions import WeChatButtonError

'''
class BaseBtn(object):

    pass
'''


class MenuBtn(object):

    def __init__(self, name, *args):

        self.json = {
            'name': name,
            'sub_button': [i.json for i in args]
        }


class ClickBtn(object):

    def __init__(self, name, key):

        self.json = {
            'type': 'click',
            'name': name,
            'key': key
        }


class ViewBtn(object):

    def __init__(self, name, url):

        self.json = {
            'type': 'view',
            'name': name,
            'url': url
        }


class ScanBtn(object):

    def __init__(self, name, key, wait_msg=False):

        self.json = {
            'type': 'scancode_waitmsg' if wait_msg else 'scancode_push',
            'name': name,
            'key': key
        }


class PhotoBtn(object):

    def __init__(self, name, key, only_sysphoto=False, only_album=False):

        btn_type = 'pic_photo_or_album'
        if only_sysphoto:
            btn_type = 'pic_sysphoto'
        elif only_album:
            btn_type = 'pic_weixin'

        self.json = {
            'type': btn_type,
            'name': name,
            'key': key
        }


# TODO 待测试
class LocationBtn(object):

    def __init__(self, name, key):

        self.json = {
            'type': 'location_select',
            'name': name,
            'key': key
        }


# TODO 待测试
class MediaBtn(object):

    def __init__(self, name, media_id, open_article=False):

        self.json = {
            'type': 'view_limited' if open_article else 'media_id',
            'name': name,
            'media_id': media_id
        }


# TODO 文档
class MatchRule(object):
    """
    https://mp.weixin.qq.com/wiki/0/c48ccd12b69ae023159b4bfaa7c39c20.html
    地区表 https://mp.weixin.qq.com/wiki/static/assets/870a3c2a14e97b3e74fde5e88fa47717.zip
    """

    def __init__(self, **kwargs):

        # TODO sex 支持 male, Female 不限制大小写，client_platform_type 同样
        for i in kwargs.keys():
            if i in ['group_id', 'sex', 'client_platform_type', 'country', 'province', 'city', 'language']:
                break
        else:
            raise WeChatButtonError(u'No valid arguments(没有有效参数)')

        if 'city' in kwargs and 'province' not in kwargs:
            raise WeChatButtonError(u'City to be set before setting the provinces(设置城市前需设置省份)')

        if 'province' in kwargs and 'country 'not in kwargs:
            raise WeChatButtonError(u'Province to be set before setting the country(设置省份前需设置国家)')

        self.json = kwargs

