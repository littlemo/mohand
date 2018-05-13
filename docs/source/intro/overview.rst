.. _intro-overview:

====
概览
====

MoHand 为通用自动化处理工具，主要用于运维自动化。

灵感来自于 Python 下很经典的运维工具 `Fabric`_ ，故您在使用中会看到很多 `Fabric`_ 的影子。

最初开发 MoHand 是为了在公司自动化登录堡垒机，由于所在公司的业务较复杂，
故需要登录全国各地的堡垒机，然后跳到对应的私有云内，进行开发&调试工作。

考虑到高扩展性，同时也是因为深知自己能力有限不可多知多能，故在设计整体架构时，
参考了 `Gulp`_ 以及 `PostCSS`_ 的组件思想，通过 Python 的 `stevedore`_
实现了高扩展性的插件系统，并自己实现了一个用于自动化登录堡垒机的插件 `mohand-plugin-expect`_ 。

如果您使用后觉得有意思，欢迎实现更多的插件分享给大家，我会及时在该文档中更新 plugin 列表，
供后来人参考&使用。若其足够优秀，我将考虑将其加入到 MoHand 的 ``install_requires`` 中！

安装方法
========

使用说明
========


.. _Fabric: http://www.fabfile.org
.. _Gulp: https://gulpjs.com
.. _PostCSS: https://postcss.org
.. _stevedore: https://docs.openstack.org/stevedore/latest/
.. _mohand-plugin-expect: http://mohand-plugin-expect.rtfd.io/
