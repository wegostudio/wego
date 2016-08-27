# -*- coding: utf-8 -*-

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
