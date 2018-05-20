# encoding=utf8
"""
用以提供全局参数的声明
"""
from __future__ import unicode_literals

from collections import OrderedDict

from mohand.utils import _AttributeDict
from mohand.version import get_cli_version


env = _AttributeDict({
    'version': OrderedDict({
        'mohand': get_cli_version(),
    }),
    'plugin_namespace': 'mohand.plugin.hand',

    # 终端再赋值
    'handfile': 'handfile.py',
})
"""
全局环境字典，包含所有的配置
部分配置，如 ``version`` ，会在加载完扩展插件后进行再次填充
"""
