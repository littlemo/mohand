"""
声明模块

用以提供全局参数的声明
"""
from collections import OrderedDict

from mohand.utils import _AttributeDict
from mohand.version import get_cli_version


"""
全局环境字典，包含所有的配置
部分终端默认值会在终端命令定义时进行再初始化赋值
"""
env = _AttributeDict({
    'version': OrderedDict({
        'mohand': get_cli_version(),
    }),
    'plugin_namespace': 'mohand.plugin.hand',

    # 终端再赋值
    'handfile': 'handfile.py',
})
