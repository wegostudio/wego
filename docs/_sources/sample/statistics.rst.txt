.. _statistics:

数据统计
===========

WEGO对微信数据统计模块的所有API进行了封装，让您享受急速且愉悦的微信开发过程

用户分析数据接口
------------------

::

    # Django
    @w.login_required
    def test_get_variation_number_of_user_api(request):
        return w.get_variation_number_of_user('2015-12-02', '2015-12-07')

    # Django
    @w.login_required
    def test_get_user_cumulate_api(request):
        return w.get_user_cumulate('2015-12-02', '2015-12-07')

必要参数
^^^^^^^^^^^
    :begin_date: "2015-12-02"
    :end_date: "2015-12-07"

注意事项
^^^^^^^^^^^
    * 接口侧的公众号数据的数据库中仅存储了2014年12月1日之后的数据，将查询不到在此之前的日期，即使有查到，也是不可信的脏数据；
    * 请开发者在调用接口获取数据后，将数据保存在自身数据库中，即加快下次用户的访问速度，也降低了微信侧接口调用的不必要损耗。

返回对象
^^^^^^^^^^^

    :return: Json object 详见 `用户分析数据接口 <https://mp.weixin.qq.com/wiki/15/88726a421bfc54654a3095821c3ca3bb.html>`_


图文分析数据接口
------------------

::

    # Django
    @w.login_required
    def test_many_api(request):
        data = w.get_article_summary('2015-12-02', '2015-12-07')
        data = w.get_article_total('2015-12-02', '2015-12-07')
        data = w.get_user_read('2015-12-02', '2015-12-07')
        data = w.get_user_read_hour('2015-12-02', '2015-12-07')
        data = w.get_user_share('2015-12-02', '2015-12-07')
        data = w.get_user_share_hour('2015-12-02', '2015-12-07')

必要参数
^^^^^^^^^^^
    :begin_date: "2015-12-02"
    :end_date: "2015-12-07"

注意事项
^^^^^^^^^^^
    * 接口侧的公众号数据的数据库中仅存储了2014年12月1日之后的数据，将查询不到在此之前的日期，即使有查到，也是不可信的脏数据；
    * 请开发者在调用接口获取数据后，将数据保存在自身数据库中，即加快下次用户的访问速度，也降低了微信侧接口调用的不必要损耗。
    * 额外注意，获取图文群发每日数据接口的结果中，只有中间页阅读人数+原文页阅读人数+分享转发人数+分享转发次数+收藏次数 >=3的结果才会得到统计，过小的阅读量的图文消息无法统计。

返回对象
^^^^^^^^^^^

    :return: Json object 详见 `图文分析数据接口 <https://mp.weixin.qq.com/wiki/9/d347c6ddb6f86ab11ec3b41c2729c8d9.html>`_



消息分析数据接口
------------------
    待开发...


接口分析数据接口
------------------
    待开发...
