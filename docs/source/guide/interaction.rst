.. _interaction:

与用户互动
==========

大部分按钮都有自己的功能，当启用服务器事件推送后，被点击的按钮会推送对应的事件到服务器，我们可以对这些事件进行回复，从而实现与用户互动。

启用服务器推送
--------------

在微信公众平台，基本配置中启用（TODO），启用时有一个简单的服务器验证过程，大部分情况下不需要进行安全验证，直接返回（TODO） 即可，启用后记得将对应的 token、aeskey 填入 wego.init 中。

响应服务器推送事件
------------------

每当用户操作了功能按钮，服务器就会收到来自微信的事件推送，我们得解析事件然后响应事件，如果启用了加密，我们还需要先解密，好在有 wego 这个过程会十分简单。

::

    @csrf_exempt
    def wechat_push(request):

        push = w.analysis_push(request)
        user = w.get_ext_userinfo(push.from_user)
        reply = push.reply_text('hello ' + user.nickname)
        return HttpResponse(reply)

wego 能解析所有的事件，由于一些事件微信命名重复，WeChatPush 包含了一个 type 属性进行严格的区分，当然，并不是所有类型的事件都能返回消息给用户，wego 的所有 type 都在 API 文档内都一一列出来，可以与用户交互的 type 在后面都有一个小勾。
