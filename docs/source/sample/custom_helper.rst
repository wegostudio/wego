定制 helper
==============

在 WEGO 中 helper 扮演了十分重要的角色，官方提供了 Django 和 Tornado 的 helper 但是你可能没有使用这两个框架或是助手不符合应用的实际情况，这时候你就需要自定义一个 helper。

注：即便是 Tornado 有官方的 helper 我们仍然建议你自定义一个 helper，因为官方 helper 由于不知道你所使用的数据库，所以只能将数据存储在加密的 cookie 中。


定制说明
----------

你可以参考官方 django helper 的源码进行定制。

::

    from wego.helpers.base_helper import BaseHelper

    class DjangoHelper(BaseHelper):

        def __init__(self, request):
            self.request = request

        def get_current_path(self):
            return self.request.get_full_path()

        def get_params(self):
            return self.request.GET.dict()

        def get_body(self):
            return self.request.body

        def set_session(self, key, value):
            self.request.session[key] = value

        def get_session(self, key):
            return self.request.session.get(key, False)

        def redirect(self, url):
            from django.shortcuts import redirect
            return redirect(url)

:__init__: 初始化时，request 为 handler 的第一个参数，如 Django 的 request , Tornado 的 self。
:get_current_path: 当调用此函数时，需要返回当前请求的 path 如果请求 http://www.example.com/a/b/c 需返回字符串的 '/a/b/c' (请保证以 '/' 开头)。
:get_params: 当调用此函数时，需要以字典形式返回当前请求的所有 GET 参数，键值对要求值为字符串而不是列表，如果是列表建议取最后一个的值: value_list[-1]。
:get_body: 当调用此函数时，需要以字符串形式返回当前请求的 body。
:set_session: 当调用此函数时会传入两个参数 key 与 value，你需要将其保存至数据库并与请求绑定。
:get_session: 当调用此函数时会传入一个参数 key，你需要返回此请求 session 中该 key 的 value。
:redirect: 当调用此函数时会，你需要返回你所使用框架的 301 跳转响应。

当你定制完成后只需将初始化参数 HELPER 的值改为你所自定义的类即可。