.. _user:

管理用户
========

微信开发过程中，获取和管理用户数据是很常见的需求


获取 WeChatUser
----------------
在 Django 或 Tornado 中，使用装饰器 @w.login_required 的函数内，第一个参数会增加一个 wx_user 的属性，如 request.wx_user 或者 self.wx_user ，这就是 WeChatUser 的实例，当然你也可以通过 w.get_ext_userinfo() 传入已关注服务号的用户 openid 来获得对应用户的 :class:`WeChatUser <wego.api.WeChatUser>` 实例。

操作 WeChatUser
-----------------

WEGO 做了很多努力，尽可能的使 WeChatUser 更智能，你可以直接从 WeChatUser 对象的属性中获取到官方返回的所有 `用户信息 <https://mp.weixin.qq.com/wiki/4/9ac2e7b1f1d22e9e57260f6553822520.html#.E7.AC.AC.E5.9B.9B.E6.AD.A5.EF.BC.9A.E6.8B.89.E5.8F.96.E7.94.A8.E6.88.B7.E4.BF.A1.E6.81.AF.28.E9.9C.80scope.E4.B8.BA_snsapi_userinfo.29>`_ ，同时，subscribe、language、remark、groupid 这些需要调用额外接口的数据你也能直接从它的属性中获取，WeChatUser 是惰性的，只有当你需要这些额外信息时它才会发出更多的请求，而且，你可以直接对它的 remark、group、groupid 这些属性赋值，对应的请求会在你赋值时发送到微信服务器。

::

    @w.login_required
    der test(request):

        user = request.wx_user
        nickname = user.nickname
        subscribe = user.subscribe
        user.remark = 'foo'
