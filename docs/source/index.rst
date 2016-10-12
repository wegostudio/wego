.. wego documentation master file, created by
   sphinx-quickstart on Sat Aug 20 14:49:18 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

WEGO:
================================

Wego 能协助你在微信开发中专注业务逻辑摆脱微信接口调试的烦恼。

看看 WEGO 到底有多方便: ::

    # django
    @w.login_required
    def index(request):
        hello = 'Hello %s!' % request.wx_user.nickname
        return HttpResponse(hello)

    # tornado
    class IndexHandler(tornado.web.RequestHandler):
        @w.login_required
        def get(self):
            hello = 'Hello %s!' % self.wx_user.nickname
            return self.write(hello)

教程
----

通过简单的教程, 你将很快上手 WEGO。

.. toctree::
   :maxdepth: 3
   
   guide/install
   guide/hello
   guide/menu
   guide/interaction
   guide/paytime

示例
----

完整、可用于生产项目的代码示例。

.. toctree::
   :maxdepth: 3
   
   sample/init
   sample/user
   sample/buttons
   sample/pay
   sample/material
   sample/custom_helper
   sample/custom_get_token

API 文档
--------------

.. toctree::
   :maxdepth: 2

   api
