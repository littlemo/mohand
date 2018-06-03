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

您可以通过 ``pip`` 进行安装，本包仅在 ``Python 3.X`` 下测试通过::

    pip3 install mohand

.. hint::

    从 ``v1.0.1`` 版本开始，增加了对 ``Python 2.X`` 的支持，但由于我主要在 **Py3**
    环境下使用，所以强烈建议您在 **Py3** 下使用。如果您在 **Py2** 环境下遇到任何异常，
    可以及时提 `Issues`_ 给我，我会努力在搬砖的间隙进行修复。。。

.. note::

    建议使用 `virtualenv`_ 来安装，避免与其他包产生依赖冲突。

    如果您感兴趣的话，可以了解下 `virtualenvwrapper`_ ，用其来管理虚拟环境可谓丝般顺滑！

使用说明
========

安装成功后，您将获得 ``mohand`` 终端命令，该命令在调用前会加载当前路径下的 ``handfile.py``
文件，若没有找到，则会递归向父级路径查找，直到根路径结束。若未找到该文件，则会返回信息如下::

    $ mohand
    [ERROR] 未找到 handfile 文件！

当其找到该文件后，会立即加载该文件，并停止继续递归。此处我们在当前路径创建该文件，然后再次执行::

    $ touch handfile.py
    $ mohand
    Usage: mohand [OPTIONS] COMMAND [ARGS]...

      通用自动化处理工具

      详情参考 `GitHub <https://github.com/littlemo/mohand>`_

    Options:
      --author   作者信息
      --version  版本信息
      --help     Show this message and exit.

此时 ``mohand`` 已经可以正常运行了，但是我们还没有可用于执行的子命令，接下来我们在
``handfile.py`` 文件中实现一个子命令::

    from mohand.hands import hand


    @hand.general
    def hello():
        """Hello World!"""
        print('Hello World!')

好，此时我们已经拥有了一个可执行的子命令，如何证明呢？再执行一次 ``mohand`` 看看吧::

    $ mohand
    Usage: mohand [OPTIONS] COMMAND [ARGS]...

      通用自动化处理工具

      详情参考 `GitHub <https://github.com/littlemo/mohand>`_

    Options:
      --author   作者信息
      --version  版本信息
      --help     Show this message and exit.

    Commands:
      hello  Hello World!

注意最后两行，现在已经多了一条子命令，其命令名即为我们之前实现的函数名，说明即该函数的 ``__doc__`` 。
这里的 CLI 是基于 `click`_ 包实现的，故您基本感受不到其存在，相关逻辑已经被封装到 ``hand.general``
这个装饰器中了。

接下来就是见证奇迹的时刻了，我们来执行以下这个子命令看看::

    $ mohand hello
    Hello World!

看我们实现的命令被执行了，打印出了 ``Hello World!`` 。

还记得我之前说过的循环递归查找 ``handfile.py`` 文件么？这个性质将很方便，比如将我们刚实现的
``handfile.py`` 移到 ``~`` 下，这样我们在 ``~`` 目录下就都可以加载到这个文件中的子命令了。

.. note::

    另外， ``mohand`` 还支持对 ``handfile`` 模块的加载，即您可以实现一个以 ``handfile``
    命名的 **Python** 包，并在其 ``__init__.py`` 中将想要被加载的命令导入，这样
    ``mohand`` 就会对其进行加载处理，并注册为子命令。

高级用法
========

由于 ``mohand`` 的终端命令方案使用的是 `click`_ ，故您可以在实现子命令时灵活的增加命令参数,
继续以上述 ``hello`` 命令为例，为其添加一个终端参数::

    @hand._click.option('--who', '-w', default='World', help='默认值为 `World` ')
    @hand.general
    def hello(who):
        """Hello World!"""
        print('Hello {}!'.format(who))

我们为 ``hello`` 命令增加了一个 ``who`` 的可选参数，该参数默认值为 ``World`` ，调用看看::

    $ mohand hello --help
    Usage: mohand hello [OPTIONS]

      Hello World!

    Options:
      -w, --who TEXT  默认值为 `World`
      --help          Show this message and exit.

    $ mohand hello
    Hello World!

    $ mohand hello -w MoHand
    Hello MoHand!

我们通过传参定制了输出的结果，您可以通过这个方法获得一个强大的命令扩展系统。

.. _Fabric: http://www.fabfile.org
.. _Gulp: https://gulpjs.com
.. _PostCSS: https://postcss.org
.. _stevedore: https://docs.openstack.org/stevedore/latest/
.. _mohand-plugin-expect: http://mohand-plugin-expect.rtfd.io/
.. _virtualenv: http://virtualenv.pypa.io/
.. _virtualenvwrapper: https://virtualenvwrapper.readthedocs.io/
.. _click: http://click.pocoo.org/6/
.. _Issues: https://github.com/littlemo/mohand/issues
