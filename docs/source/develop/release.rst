.. _develop-release:

========
发布说明
========

v1.1.1 (2018-09-06 10:30:30)
----------------------------

Bugfix
~~~~~~

#. 修复当未安装插件包时，加载插件逻辑执行失败的 Bug


v1.1.0 (2018-06-03 20:05:43)
----------------------------

Feature
~~~~~~~

#. 实现默认支持的 ``hand`` 装饰器 ``general`` ，用以提供基础的子命令注册功能
#. 增强对 ``Python2.X`` 的兼容性
#. 去除对子插件 ``mohand-plugin-expect`` 的依赖

Bugfix
~~~~~~

#. 修复对 ``handfile`` 模块的加载失败 Bug


v1.0.1 (2018-05-19 12:15:06)
----------------------------

Feature
~~~~~~~

#. 增加了对 ``Python 2.X`` 的支持


v1.0.0 (2018-05-13 23:02:46)
----------------------------

Feature
~~~~~~~

#. 实现 ``mohand`` 终端命令
#. 实现对 ``handfile.py`` 文件的递归查找并加载
#. 实现 ``mohand`` 子命令的注册
#. 实现扩展插件的加载&注册
#. 实现全局参数声明管理模块
