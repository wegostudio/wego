.. _material:

素材管理
===========

WEGO对微信素材管理模块的所有API进行了封装，让您享受急速且愉悦的微信开发过程

在此之前
-----------

初始化生成 w 实例时，请记得将所需参数填入， 详见初始化 :ref:`init`


新增临时素材
--------------

::

    # Django
    @w.login_required
    def test_add_temporary_material_api(request):
        with open('/path/to/media.png') as f: 
            w.add_temporary_material(type='image', media=f)

必要参数
^^^^^^^^^^^
    :type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb，主要用于视频与音乐格式的缩略图）
    :media: python文件对象

注意事项
^^^^^^^^^^^
    上传的临时多媒体文件有格式和大小限制，如下：

    * 图片（image）: 2M，支持bmp/png/jpeg/jpg/gif格式
    * 语音（voice）：2M，播放长度不超过60s，支持AMR\MP3格式
    * 视频（video）：10MB，支持MP4格式
    * 缩略图（thumb）：64KB，支持JPG格式

返回对象
^^^^^^^^^^^

    :return: Json object 详见 `新增临时素材 <https://mp.weixin.qq.com/wiki/15/2d353966323806a202cd2deaafe8e557.html>`_
    **注意：** 成功时返回的Json中有media_id，建议将其保存

获取临时素材
--------------

::

    # Django
    @w.login_required
    def test_get_temporary_material_api(request):
        media = w.get_temporary_material(media_id=u'your_media_id')
        if media:
            # 获取临时素材成功，将其保存到本地
            with open('/path/to/save/media.*', 'wb') as f:
                f.write(media)
        else:
            # TODO获取临时素材失败

必要参数
^^^^^^^^^^^
    :media_id: 媒体文件ID

返回对象
^^^^^^^^^^^
    :success return: File object
    :fail return: None


新增永久素材
--------------
    最近更新，永久图片素材新增后，将带有URL返回给开发者，开发者可以在腾讯系域名内使用（腾讯系域名外使用，图片将被屏蔽），以下是实例代码。

::

    # Django
    articles: [{
        "title": u'测试',
        "thumb_media_id": u'CrRA4_7jU0pIxXW9U-90C8ixLOfcw2wJYew-wzZ34kQ',
        "author": u'测试人员',
        "digest": u'测试',
        "show_cover_pic": '1',
        "content": u'测试',
        "content_source_url": 'www.placehold.com'
    }, {
        "title": u'测试',
        "thumb_media_id": u'CrRA4_7jU0pIxXW9U-90C8ixLOfcw2wJYew-wzZ34kQ',
        "author": u'测试人员',
        "digest": u'测试',
        "show_cover_pic": '1',
        "content": u'测试',
        "content_source_url": 'www.placehold.com'
    },
    # 若新增的是多图文素材，则此处应有几段articles结构，最多8段
    ]

    @w.login_required
    def test_add_permanent_material_api(request):
        return w.add_permanent_material(articles)

注意事项
^^^^^^^^^^^^

    * 新增的永久素材也可以在公众平台官网素材管理模块中看到
    * 永久素材的数量是有上限的，请谨慎新增。图文消息素材和图片素材的上限为5000，其他类型为1000
    * 素材的格式大小等要求与公众平台官网一致。具体是，图片大小不超过2M，支持bmp/png/jpeg/jpg/gif格式，语音大小不超过5M，长度不超过60秒（公众平台官网可以在文章中插入小于30分钟的语音，但这些语音不能用于群发等场景，只能放在文章内，这方面接口暂不支持），支持mp3/wma/wav/amr格式
    * 调用该接口需https协议

必要参数
^^^^^^^^^^^
    :articles: list对象，存dict，dict的必要键：title， thumb_media_id，author， digest， show_cover_pic， content，content_source_url

返回对象
^^^^^^^^^^^

    :success return: Json object { "media_id":MEDIA_ID }
    :fail return: {"errcode":40007,"errmsg":"ERROR"}
    **注意：** 成功时返回的Json中的media_id，建议将其保存

上传图文消息内的图片获取URL
----------------------------
    请注意，本接口所上传的图片不占用公众号的素材库中图片数量的5000个的限制。图片仅支持jpg/png格式，大小必须在1MB以下。

::

    # Django
    @w.login_required
    def test_upload_content_picture_api(request):
        with open('/path/to/media.png') as f: 
            w.pload_content_picture(media=f)

必要参数
^^^^^^^^^^^
    :media: python文件对象

返回对象
^^^^^^^^^^^

    :success return: Json object {"url":  "URL"}
    **注意：** 成功时返回的Json中有url，建议将其保存

新增其他永久素材
-----------------

::

    # Django
    @w.login_required
    def test_add_other_material_api(request):
        with open('/path/to/media.png') as f: 
            w.add_other_material(type='image', media=f)
            # 上传视频文件
            # w.add_other_material(type='image', media=f, title='TITLE', introduction="INTRODUCTION")

必要参数
^^^^^^^^^^^
    :type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb，主要用于视频与音乐格式的缩略图）
    :media: python文件对象

当上传视频文件时的必要参数
^^^^^^^^^^^
    :title: 视频素材的标题
    :introduction: 视频素材的描述

返回对象
^^^^^^^^^^^

    :success return: Json object {"media_id":MEDIA_ID, "url":URL }
    :fail return: {"errcode":40007,"errmsg":"invalid media_id"}
    **注意：** 成功时返回的Json中有media_id，建议将其保存

获取永久素材
--------------

::

    # Django
    @w.login_required
    def test_get_permanent_material_api(request):
        return w.get_temporary_material(media_id=u'your_media_id')

必要参数
^^^^^^^^^^^
    :media_id: 媒体文件ID

返回对象
^^^^^^^^^^^
    :return: Json object 返回值详见 `获取永久素材 <https://mp.weixin.qq.com/wiki/12/3c12fac7c14cb4d0e0d4fe2fbc87b638.html>`_

删除永久素材
--------------
    在新增了永久素材后，使用WEGO的开发者可以调用该接口删除不再需要的永久素材，节省空间，以下是代码示例

::

    # Django
    @w.login_required
    def test_delete_material_api(request):
        return w.delete_material(media_id=u'your_media_id')

注意事项
^^^^^^^^^^^^

    * 请谨慎操作本接口，因为它可以删除公众号在公众平台官网素材管理模块中新建的图文消息、语音、视频等素材（但需要先通过获取素材列表来获知素材的media_id）
    * 临时素材无法通过本接口删除
    * 调用该接口需https协议

必要参数
^^^^^^^^^^^
    :media_id: 媒体文件ID

返回对象
^^^^^^^^^^^
    :return: Json object ->{"errcode":ERRCODE, "errmsg":ERRMSG } (正常情况下调用成功时，errcode将为0)


修改永久素材
--------------

::

    # Django
    @w.login_required
    def test_update_material_api(request):
        return w.update_material(
            media_id=MEDIA_ID,
            index=INDEX,
            title=TITLE,
            thumb_media_id=THUMB_MEDIA_ID,
            author=AUTHOR,
            digest=DIGEST,
            show_cover_pic=SHOW_COVER_PIC(0 / 1),
            content=CONTENT,
            content_source_url=CONTENT_SOURCE_URL
        )

注意事项
^^^^^^^^^^^^

    * 也可以在公众平台官网素材管理模块中保存的图文消息（永久图文素材）
    * 调用该接口需https协议

必要参数
^^^^^^^^^^^
    :media_id: 要修改的图文消息的id
    :index: 要更新的文章在图文消息中的位置（多图文消息时，此字段才有意义），第一篇为0
    :title: 标题
    :thumb_media_id: 图文消息的封面图片素材id（必须是永久mediaID)
    :author: 作者
    :digest: 图文消息的摘要，仅有单图文消息才有摘要，多图文此处为空
    :show_cover_pic: 是否显示封面，0为false，即不显示，1为true，即显示
    :content: 图文消息的具体内容，支持HTML标签，必须少于2万字符，小于1M，且此处会去除JS
    :content_source_url: 图文消息的原文地址，即点击“阅读原文”后的URL

返回对象
^^^^^^^^^^^
    :return: Json object ->{"errcode":ERRCODE, "errmsg":ERRMSG } (正常情况下调用成功时，errcode将为0)


获取素材总数
--------------

::

    # Django
    @w.login_required
    def test_get_materials_count_api():
        data = w.get_materials_count()

        """
        if success:
        data = {
            u'voice_count': 0,
            u'video_count': 1,
            u'image_count': 72,
            u'news_count': 12
        }
        """

返回对象
^^^^^^^^^^

    :success return: Json object: {"voice_count":COUNT, "video_count":COUNT, "image_count":COUNT, "news_count":COUNT }
    :fail return: Json object: {"errcode":-1,"errmsg":"system error"}


获取素材列表
--------------

::

    # Django
    @w.login_required
    def test_get_materials_list_api():
        data = w.get_materials_list(
            material_type='image',
            offset=0,
            count=1
        )

必要参数
^^^^^^^^^^^
    :material_type: 素材的类型，图片（image）、视频（video）、语音 （voice）、图文（news）
    :offset: 从全部素材的该偏移位置开始返回，0表示从第一个素材 返回
    :count: 返回素材的数量，取值在1到20之间

返回对象
^^^^^^^^^^

    :return: Json object （具体返回值请参考 `获取素材列表 <https://mp.weixin.qq.com/wiki/15/8386c11b7bc4cdd1499c572bfe2e95b3.html>`_）
