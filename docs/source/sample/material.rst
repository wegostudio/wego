.. _material:

素材管理
===========

WEGO对微信素材管理模块的的所有API进行了封装，让您享受急速且愉悦的微信开发过程

在此之前
-----------

初始化生成 w 实例时，请记得将所需参数填入， 详见初始化 :ref:`init`


新增临时素材
--------------


::

    # Django
    @w.login_required
    def add_temporary_material(request):
        f = {'file': open('/path/to/media.png')}
        return w.add_temporary_material(type='image', media=f)

必要参数
^^^^^^^^^^^
    :type: 媒体文件类型，分别有图片（image）、语音（voice）、视频（video）和缩略图（thumb，主要用于视频与音乐格式的缩略图）

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
    def get_temporary_material(request):
        media = w.get_temporary_material(media_id=u'your_media_id')
        if media:
            with open('/path/to/save/media', 'wb') as f:
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


新增永久素材   ....未完成
--------------
    最近更新，永久图片素材新增后，将带有URL返回给开发者，开发者可以在腾讯系域名内使用（腾讯系域名外使用，图片将被屏蔽）。

::

    # Django
    @w.login_required
    def add_permanent_material(request):
        w.add_permanent_material(

        )

注意事项
^^^^^^^^^^^^

    * 新增的永久素材也可以在公众平台官网素材管理模块中看到
    * 永久素材的数量是有上限的，请谨慎新增。图文消息素材和图片素材的上限为5000，其他类型为1000
    * 素材的格式大小等要求与公众平台官网一致。具体是，图片大小不超过2M，支持bmp/png/jpeg/jpg/gif格式，语音大小不超过5M，长度不超过60秒（公众平台官网可以在文章中插入小于30分钟的语音，但这些语音不能用于群发等场景，只能放在文章内，这方面接口暂不支持），支持mp3/wma/wav/amr格式
    * 调用该接口需https协议


获取素材总数
--------------

::

    # Django
    @w.login_required
    def get_materials_count():
        data = w.get_materials_count()
        """if success:
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