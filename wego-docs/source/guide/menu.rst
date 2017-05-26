.. _user:

创建菜单
=========

服务号的菜单是和用户交互最直接的部分，在启用服务器事件推送后，微信公众平台将不能在后台设置菜单，但是在 WEGO，菜单设置一样很简单。我们推荐创建菜单的代码紧跟在 wego.init 之后，这样才能保证最新的菜单在每次启动 web 服务时创建。

创建菜单 ::

    # 根据需要 import 所需的按钮
    from wego.buttons import *
    

    w.create_menu(
        ViewBtn(u'点击跳转', 'click msg0'),
        MenuBtn(
            u'菜单',
            ClickBtn(u'点击按钮', 'click msg1')
        )
    )

按钮最多能创建三个，并且菜单只有一级，菜单内最多能包含五个按钮。WEGO 可以创建目前支持创建的所有按钮，具体请看 :ref:`Buttons <buttons>`。
