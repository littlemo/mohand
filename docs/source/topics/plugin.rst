.. _topics-plugin:

========
插件实现
========

实现您自己的 **hand** 插件并不难，您可以参考GitHub上 `mohand-plugin-expect`_ 的实现。
您需要做的事情如下:

#. 实现一个 ``mohand.hands.HandBase`` 的子类，用于注册您的 **hand** 装饰器、提供版本信息
#. 实现一个 hand ，如 `mohand-plugin-expect`_ 中的 ``hand.expect``
#. 在 ``setup.py`` 中添加一个 ``mohand.plugin.hand`` 的 **entry_points**


插件列表
========

您可以直接通过名称进行 ``pip`` 安装

`mohand-plugin-expect`_
    可用于自动化登录堡垒机完成跳转选择、账户密码输入等操作

`mohand-plugin-otp`_
    可用于提供定制化的一次性密码生成服务


.. _mohand-plugin-expect: https://github.com/littlemo/mohand-plugin-expect
.. _mohand-plugin-otp: https://github.com/littlemo/mohand-plugin-otp
