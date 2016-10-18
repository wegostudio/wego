# -*- coding: utf-8 -*-
from .exceptions import WegoApiError, WeChatUserError
from functools import reduce
import wego
import json
import time
import random
import string
import hashlib


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
            openid = None

            if code:
                openid = self.get_openid(helper, code)
                helper.set_session('wx_openid', openid)

            if not openid:
                openid = helper.get_session('wx_openid')

            if openid:
                request.wego = self
                request.wx_openid = openid

                wx_user = self.get_userinfo(helper, openid)
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

        state = 'WEGO'
        if self.settings.REDIRECT_PATH:
            redirect_url = self.settings.REDIRECT_PATH
            if self.settings.REDIRECT_STATE:
                state = self.settings.REDIRECT_STATE
        else:
            redirect_url = helper.get_current_path()
            get_params = helper.get_params()
            if 'code' not in get_params:
                state = '&'.join(['%s=%s' % (i, j) for i, j in get_params.items()])
        url = self.wechat.get_code_url(redirect_url, state)

        return helper.redirect(url)

    def get_openid(self, helper, code):
        """
        Get user openid.

        :param code: A code that user redirect back will bring.
        :return: openid
        """

        data = self.wechat.get_access_token(code)

        self._set_user_tokens(helper, data)

        return data['openid']

    def get_userinfo(self, helper, openid):
        """
        Get user info.

        :return: :class:`WeChatUser <wego.api.WeChatUser>` object
        """

        wechat_user = self._get_userinfo_from_session(helper)
        if wechat_user:
            return wechat_user

        wx_access_token_expires_at = helper.get_session('wx_access_token_expires_at')
        if wx_access_token_expires_at and float(wx_access_token_expires_at) < time.time():
            refresh_token = helper.get_session('wx_refresh_token')
            new_token = self.wechat.refresh_access_token(refresh_token)
            if new_token == 'error':
                return 'error'
            self._set_user_tokens(helper, new_token)

        access_token = helper.get_session('wx_access_token')
        data = self.wechat.get_userinfo_by_token(openid, access_token)
        self._set_userinfo_to_session(helper, data)

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
        helper.set_session('wx_access_token_expires_at', str(time.time() + data['expires_in'] - 180))
        helper.set_session('wx_refresh_token', data['refresh_token'])

    def get_ext_userinfo(self, openid):
        """
        Get user extra info, such as subscribe, language, remark and groupid.

        :return: :dict: User data
        """

        data = self.wechat.get_userinfo(openid)

        return WeChatUser(self, data)

    def verification_token(self, openid, access_token):
        """
        Determine whether the user access token has expired

        :param openid: User openid.
        :param access_token: function get_access_token returns.
        :return: Bool.
        """

        data = self.wechat.is_access_token_has_expired(openid, access_token)

        return data['errmsg'] == 'ok'

    # TODO 看看是否有必要放入一个新的类里面
    # 统一下单
    def unified_order(self, **kwargs):
        """ 
        # TODO
        Unifiedorder settings, get wechat config at https://api.mch.weixin.qq.com/pay/unifiedorder
        You can take return value as wechat api onBridgeReady's parameters directly

        You don't need to include appid, mch_id, nonce_str and sign because these three parameters set by WeChatApi,
        but the following parameters are necessary, you must be included in the kwargs
        and you must follow the format below as the parameters's key

        :param openid: User openid.

        :param body: Goods are simply described, the field must be in strict accordance with the
         specification, specific see parameters

        :param out_trade_no: Merchants system internal order number, within 32 characters,
         can include letters, other see merchant order number

        :param total_fee: Total amount of orders, the unit for points, as shown in the payment amount

        :param spbill_create_ip: APP and web payment submitted to client IP, Native fill call
         WeChat payment API machine IP.

        :param notify_url: (optional) Default is what you set at init.
            Receive pay WeChat asynchronous notification callback address,
            notify the url must be accessible url directly, cannot carry parameters.

        :param trade_type: Values are as follows: the JSAPI, NATIVE APP, details see parameter regulation

        :return: {'appId': string,
                'timeStamp': value,
                'nonceStr': value,
                'package': value,
                'signType': value,
                'paySign': value,}
        """

        default_data = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
            'notify_url': self.settings.PAY_NOTIFY_URL,
            'trade_type': 'JSAPI',
        }

        data = dict(default_data, **kwargs)
        if self.settings.DEBUG:
            data['total_fee'] = 1
        data['sign'] = self.make_sign(data)

        self._check_params(
            data,
            'appid',
            'mch_id',
            'nonce_str',
            'body',
            'out_trade_no',
            'total_fee',
            'spbill_create_ip',
            'notify_url',
            'trade_type')

        order_info = self.wechat.unified_order(data)
        if 'result_code' not in order_info or order_info['result_code'] != 'SUCCESS':
            return self.settings.LOGGER.warn(u'统一下单失败! \n传入数据:\n{}\n返回数据:\n{}'.format(
                json.dumps(data, indent=2),
                json.dumps(order_info, indent=2)
            ))

        data = {
            'appId': order_info['appid'],
            'timeStamp': str(int(time.time())),
            'nonceStr': order_info['nonce_str'],
            'package': 'prepay_id=' + order_info['prepay_id'],
            'signType': 'MD5'
        }
        data['paySign'] = self.make_sign(data)

        return data

    # 查询订单
    def query_order(self, out_trade_no=None, transaction_id=None):
        """
        # TODO https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2
        Order query setting, get wechat config at https://api.mch.weixin.qq.com/pay/orderquery
        Choose one in out_trade_no and transaction_id as parameter pass to this function

        :param out_trade_no | transaction_id: WeChat order number, priority in use.
            Merchants system internal order number, when didn't provide transaction_id need to pass this.

        :return: {...}
        """

        default_settings = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
        }
        if out_trade_no:
            default_settings['out_trade_no'] = out_trade_no
        elif transaction_id:
            default_settings['transaction_id'] = transaction_id
        else:
            raise WegoApiError('Missing required parameters "{param}" (缺少必须的参数 "{param}")'.format(
                param='out_trade_no|transaction_id'
            ))

        default_settings['sign'] = self.make_sign(default_settings)
        data = self.wechat.query_order(default_settings)

        return data

    # 关闭订单
    def close_order(self, out_trade_no):
        """
        # TODO return bool?
        Close order, get wechat config at https://api.mch.weixin.qq.com/pay/closeorder

        :param out_trade_no: Merchant order number within the system

        :return: {...}
        """

        data = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
            'out_trade_no': out_trade_no,
        }
        data['sign'] = self.make_sign(data)
        data = self.wechat.close_order(data)

        return data

    # 申请退款
    def refund_order(self, **kwargs):
        """
        Merchant order number within the system, get wechat config at https://api.mch.weixin.qq.com/secapi/pay/refund

        Following parameters are necessary, you must be included in the kwargs and you must follow the format below as the parameters's key

        :param out_trade_no or transaction_id: WeChat order number, priority in use. Merchants system internal order number, when didn't provide transaction_id need to pass this.

        :param out_refund_no: Merchants system within the refund number,
            merchants within the system, only the same refund order request only a back many times

        :param total_fee: Total amount of orders, the unit for points, only as an integer, see the payment amount

        :param refund_fee: Refund the total amount, total amount of the order,
            the unit for points, only as an integer, see the payment amount

        :param op_user_id: Operator account, the default for the merchants

        :return: {...}
        """

        default_settings = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
        }

        if 'op_user_id' not in kwargs:
            kwargs['op_user_id'] = self.settings.MCH_ID

        data = dict(default_settings, **kwargs)
        if self.settings.DEBUG:
            data['total_fee'] = 1
        data['sign'] = self.make_sign(data)
        self._check_params(
            data,
            'appid',
            'mch_id',
            'nonce_str',
            'sign',
            'out_refund_no',
            'total_fee',
            'refund_fee',
            'op_user_id'
        )

        if 'out_trade_no' not in kwargs and 'transaction_id' not in kwargs:
            raise WegoApiError('Missing required parameters "{param}" (缺少必须的参数 "{param}")'.format(
                param='out_trade_on|transaction_id'
            ))

        data = self.wechat.refund_order(data)

        return data

    # 查询退款
    def query_refund(self, **kwargs):
        """
        get wechat config at https://api.mch.weixin.qq.com/pay/refundquery

        :param transaction_id | out_trade_no | out_refund_no | refund_id: One out of four
        :return: dict {...}
        """

        default_settings = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
        }

        keys = ['transaction_id', 'out_trade_no', 'out_refund_no', 'refund_id']
        for i in keys:
            if i in kwargs:
                break
        else:
            raise WegoApiError('Missing required parameters "{param}" (缺少必须的参数 "{param}")'.format(
                param='out_trade_on|transaction_id|out_refund_no|refund_id'
            ))

        data = dict(default_settings, **kwargs)
        data['sign'] = self.make_sign(data)
        data = self.wechat.query_refund(data)

        return data

    # 下载对账单
    def download_bill(self, **kwargs):
        """
        get wechat config at https://api.mch.weixin.qq.com/pay/downloadbill

        :param bill_date:

        :param bill_type:

        :return: dict {...}
        """

        default_settings = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
        }

        data = dict(default_settings, **kwargs)
        data['sign'] = self.make_sign(data)
        self._check_params(
            data,
            'appid',
            'mch_id',
            'nonce_str',
            'sign',
            'bill_date',
            'bill_type')

        data = self.wechat.download_bill(data)

        return data

    # TODO 暂时无需
    # 交易保障
    def pay_report(self, **kwargs):
        """
        get wechat config at https://api.mch.weixin.qq.com/payitil/report

        :param interface_url:
        :param execute_time:
        :param return_code:
        :param result_code:
        :param user_ip:
        :return: dict{...}
        """

        default_settings = {
            'appid': self.settings.APP_ID,
            'mch_id': self.settings.MCH_ID,
            'nonce_str': self._get_random_code(),
        }

        data = dict(default_settings, **kwargs)
        data['sign'] = self.make_sign(data)

        self._check_params(
            data,
            'appid',
            'mch_id',
            'nonce_str',
            'sign',
            'interface_url',
            'execute_time',
            'return_code',
            'result_code',
            'user_ip'
        )

        data = self.wechat.pay_report(data)

        return data

    def _check_params(self, params, *args):
        """
        Check if params is available

        :param params: a dict.
        :return: None
        """

        for i in args:
            if i not in params or not params[i]:
                raise WegoApiError('Missing required parameters "{param}" (缺少必须的参数 "{param}")'.format(param=i))

    def _get_random_code(self):
        """
        Get random code
        """

        return reduce(lambda x, y: x + y, [random.choice(string.printable[:62]) for i in range(32)])

    def make_sign(self, data):
        """
        Generate wechat pay for signature
        """

        temp = ['%s=%s' % (k, data[k]) for k in sorted(data.keys())]
        temp.append('key=' + self.settings.MCH_SECRET)
        temp = '&'.join(temp)
        md5 = hashlib.md5()
        md5.update(temp.encode('utf-8'))

        return md5.hexdigest().upper()

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

    def get_user_groups(self, openid):
        """
        Get user groups.

        :return: :dict: {'your_group_id': {'name':'str', 'count':'int'}}
        """

        data = self.wechat.get_user_groups(openid)
        return data

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

        if groupid not in groups:
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

    def change_user_group(self, openid, group):
        """
        Change user group.

        :param group: Group id or group name.
        :return: :Bool .
        """

        groupid = self._get_groupid(group)
        data = self.wechat.change_user_group(openid, groupid)
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

    def create_menu(self, *args, **kwargs):
        """
        Create menu by wego.button

        :return: :Bool
        """

        data = {
            'button': [i.json for i in args]
        }

        if 'match' in kwargs:
            data['matchrule'] = kwargs['match'].json
            data = self.wechat.create_conditional_menu(data)
        else:
            data = self.wechat.create_menu(data)

        return not data['errcode'] if 'errcode' in data else data['menuid']

    def get_menus(self):

        data = self.wechat.get_menus()
        if 'errcode' in data and data['errcode'] == 46003:
            return {'menu': {}}
        return data

    def del_menu(self, target='all'):

        if target == 'all':
            return not self.wechat.del_all_menus()['errcode']

        return not self.wechat.del_conditional_menu(int(target))['errcode']

    def analysis_push(self, request):
        """
        Analysis xml to dict and set wego push type.
        Wego defind WeChatPush type (which can reply has checked):

            -- pay --

            all ✓

            -- msg --

            text ✓

            image ✓

            voice ✓

            video ✓

            shortvideo ✓

            location ✓

            link ✓

            -- event --

            subscribe ✓'

            unsubscribe

            scancode_push

            scancode_waitmsg ✓

            scan

            scan_subscribe

            user_location ✓

            click ✓

            view

        :param raw_xml: Raw xml.
        :return: :class:`WeChatPush <wego.api.WeChatPush>` object.
        :rtype: WeChatPush.
        """

        helper = self.settings.HELPER(request)
        raw_xml = helper.get_body()

        if raw_xml.find('return_code') != -1:
            # TODO 通知验证
            data = self.wechat._analysis_xml(raw_xml)
            return WeChatPay(data)

        crypto = None
        nonce = None

        if self.settings.PUSH_TOKEN:
            if not hasattr(self, 'push_crypto'):
                from .lib.WEGOBizMsgCrypt import WXBizMsgCrypt
                self.push_crypto = WXBizMsgCrypt(
                    self.settings.PUSH_TOKEN,
                    self.settings.PUSH_ENCODING_AES_KEY,
                    self.settings.APP_ID
                )

            crypto = self.push_crypto
            msg_sign = helper.get_params()['msg_signature']
            timestamp = helper.get_params()['timestamp']
            nonce = helper.get_params()['nonce']
            ret, raw_xml = self.push_crypto.DecryptMsg(raw_xml, msg_sign, timestamp, nonce)

        data = self.wechat._analysis_xml(raw_xml)

        return WeChatPush(data, crypto, nonce)

    def add_temporary_material(self, **kwargs):

        data = self.wechat.add_temporary_material(**kwargs)

        return data

    def get_temporary_material(self, media_id):

        data = self.wechat.get_temporary_material(media_id)

        return data

    def add_permanent_material(self, articles):

        data = self.wechat.add_permanent_material(articles)

        return data

    def upload_content_picture(self, media):

        data = self.wechat.upload_content_picture(media)

        return data

    def add_other_material(self, **kwargs):

        data = self.wechat.add_other_material(**kwargs)

        return data

    def get_permanent_material(self, media_id):

        data = self.wechat.get_permanent_material(media_id)

        return data

    def delete_material(self, media_id):

        data = self.wechat.delete_material(media_id)

        return data

    def update_material(self, **kwargs):

        data = self.wechat.update_material(**kwargs)

        return data

    def get_materials_count(self):

        data = self.wechat.get_materials_count()

        return data

    def get_materials_list(self, material_type, offset, count):

        data = self.wechat.get_materials_list(material_type, offset, count)

        return data

    def create_qrcode(self, key, expire=None):

        if expire:
            data = self.wechat.create_scene_qrcode(key, expire)

        elif type(key) is str:
            data = self.wechat.create_limit_scene_qrcode(key)

        else:
            data = self.wechat.create_limit_str_scene_qrcode(key)

        # TODO 容错
        data['code_url'] = 'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=' + data['ticket']
        return data

    def create_short_url(self, url):

        data = self.wechat.create_short_url(url)

        # TODO 容错
        return data['short_url']

    def get_wechat_servers_list(self):
        """
        Get wechat servers list

        :return: :list
        """

        data = self.wechat.get_wechat_servers_list()

        return data

    def check_personalized_menu_match(self, user_id):
        """
        Check whether personalized menu match is correct.

        :param data:user_id
        :return: :dict
        """

        data = self.wechat.check_personalized_menu_match(user_id)

        return data

    def get_variation_number_of_user(self, begin_date, end_date):
        """
        Get Variation on number of user

        :param data:begin_date, end_date
        :return: :dict
        """
        data = self.wechat.get_variation_number_of_user(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_user_cumulate(self, begin_date, end_date):
        """
        GET accumulation of user

        :param date:begin_date, end_date
        :return: :dict
        """
        data = self.wechat.get_user_cumulate(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_article_summary(self, begin_date, end_date):
        """
        Get article summary

        :param date:begin_date, end_date
        :return: :dict
        """

        data = self.wechat.get_article_summary(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_article_total(self, begin_date, end_date):
        """
        Get article total

        :param data: begin_date, end_date
        :return: :dict
        """

        data = self.wechat.get_article_total(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_user_read(self, begin_date, end_date):
        """
        Get user read

        :param data:begin_date, end_date
        :return : :dict
        """

        data = self.wechat.get_user_read(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_user_read_hour(self, begin_date, end_date):
        """
        Get user read hour

        param data:begin_date, end_date
        return : :dict
        """

        data = self.wechat.get_user_read_hour(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_user_share(self, begin_date, end_date):
        """
        Get user share

        param data:begin_data,end_date
        return : :dict
        """
        data = self.wechat.get_user_share(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data

    def get_user_share_hour(self, begin_date, end_date):
        """
        Get user share

        param data:begin_date, end_date
        retur : :dict
        """
        data = self.wechat.get_user_share_hour(begin_date, end_date)
        if 'errcode' in data:
            if data['errcode'] == 61501:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数跨度异常。)')
            elif data['errcode'] == 61500:
                raise WegoApiError(data['errmsg'] + u'(错误返回码：' + str(data['errcode']) + u'，时间参数格式异常。)')

        return data


class WeChatPay(object):

    def __init__(self, data):

        self.is_pay = True
        self.data = data
        self.return_tpl = ('<xml>' +
            '<return_code><![CDATA[SUCCESS]]></return_code>' +
            '<return_msg><![CDATA[%s]]></return_msg>' +
        '</xml>')
        self.success = self.return_tpl % 'OK'

    def fail(self, text):
        return self.return_tpl % text
 
    def __getattr__(self, key):

        if key in self.data:
            return self.data[key]
        return ''


class WeChatPush(object):
    """
    """

    def __init__(self, data, crypto=None, nonce=None):

        self.data = data
        self.crypto = crypto
        self.nonce = nonce

        if data['MsgType'] == 'event':
            if data['Event'] == 'subscribe' and 'Ticket' in data:
                self.type = 'scan_subcribe'
            elif data['Event'] == 'LOCATION':
                self.type = 'user_location'
            else:
                self.type = data['Event'].lower()
        else:
            self.type = data['MsgType']

        self.from_user = data['FromUserName']
        self.to_user = data['ToUserName']

    def return_xml(self, data):

        data['ToUserName'] = self.from_user
        data['FromUserName'] = self.to_user
        data['CreateTime'] = int(time.time())

        xml = wego.wechat.WeChatApi._make_xml(data)

        if self.nonce:
            ret, xml = self.crypto.EncryptMsg(xml, self.nonce)

        return xml

    def __getattr__(self, key):

        if key in self.data:
            return self.data[key]
        return ''

    def reply_text(self, text):

        return self.return_xml({
            'MsgType': 'text',
            'Content': text
        })

    def reply_image(self, image):

        return self.return_xml({
            'MsgType': 'image',
            'Image': {'MediaId': image}
        })

    def reply_voice(self, voice):

        return self.return_xml({
            'MsgType': 'voice',
            'Voice': {'MediaId': voice}
        })

    def reply_video(self, video):

        # TODO 视频要等审核通过才能用, 或者是永久素材
        data = {
            'MediaId': video['media_id']
        }
        if 'title' in video:
            data['Title'] = video['title']
        if 'description' in video:
            data['Description'] = video['description']

        return self.return_xml({
            'MsgType': 'video',
            'Video': data
        })

    def reply_music(self, music):

        data = {
            'Title': music['title'],
            'Description': music['description'],
            'MusicUrl': music['music_url'],
            'HQMusicUrl': music['hq_music_url'],
        }
        if 'thumb_media_id' in music:
            data['ThumbMediaId'] = music['thumb_media_id']

        return self.return_xml({
            'MsgType': 'music',
            'Music': data
        })

    def reply_news(self, news):

        data = []
        for i in news:
            new_dict = {}
            if 'title' in i:
                new_dict['Title'] = i['title'],
            if 'description' in i:
                new_dict['Description'] = i['description'],
            if 'pic_url' in i:
                new_dict['PicUrl'] = i['pic_url'],
            if 'url' in i:
                new_dict['Url'] = i['url'],
            data.append(new_dict)

        return self.return_xml({
            'MsgType': 'news',
            'ArticleCount': len(news),
            'Articles': {
                'item': data
            }
        })


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

        if key == 'group' and key not in self.data:
            self.data['group'] = self.wego.get_groups()[self.groupid]

        if key in self.data:
            return self.data[key]
        return ''

    def __setattr__(self, key, value):

        if key == 'remark':
            if self.subscribe != 1:
                raise WeChatUserError('The user does not subscribe you')

            if self.data['remark'] != value:
                self.wego.wechat.set_user_remark(self.data['openid'], value)
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
            if groupid not in groups:
                raise WeChatUserError(u'Without this group(没有这个群组)')

            self.wego.change_user_group(self.data['openid'], groupid)

        super(WeChatUser, self).__setattr__(key, value)

    def get_ext_userinfo(self):
        """
        Get user extra info, such as subscribe, language, remark and groupid.

        :return: :dict: User data
        """

        self.data['remark'] = ''
        self.data['groupid'] = ''

        data = self.wego.wechat.get_userinfo(self.data['openid'])
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

    if not self.global_access_token or self.global_access_token['expires_at'] <= int(time.time()):
        self.global_access_token = self.get_global_access_token()
        self.global_access_token['expires_at'] = self.global_access_token['expires_in'] + int(time.time()) - 180

    return self.global_access_token['access_token']
