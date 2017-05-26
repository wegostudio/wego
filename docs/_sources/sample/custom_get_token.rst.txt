定制 get_global_access_token
============================

微信接口调用中有一个 access token，它是一个全局 token，为把它与 OAuth 中的 code 换取的 access token 区别开我们称之为 global access token。定制 get_global_access_token 函数在分布式系统中显得十分必要，因为每次调用接口都会使之前获得的 global access token 过期，只有最后一次调用接口时获取到的 global access token 是有效的。

定制说明
----------
你可以参考官方 get_global_access_token 的源码进行定制。

::

    def official_get_global_access_token(self):
        """
        Get global access token.

        :param self: Call self.get_global_access_token() for get global access token.
        :return: :str: Global access token
        """

        if not self.global_access_token or self.global_access_token['expires_at'] <= int(time.time()):
            self.global_access_token = self.get_global_access_token()
            self.global_access_token['expires_at'] += int(time.time()) - 180

        return self.global_access_token['access_token']

每当需要获取 global access token 时，都会调用此函数，函数需要返回一个可用的 global access token，当你需要自定义时，你应当把 global access token 以及过期时间存入数据库中，函数每次被调用时应当先检查是否过期，如果过期则调用 self.get_global_access_token() 重新获取 global access token 。

self.get_global_access_token() 返回一个字典，字典内包含 access_token 及 expires_in:

:access_token: global access token
:expires_in: 有效时间，单位为秒，为了保证调用的可靠性，我们建议在有效时间的基础上减去 180 秒