# encoding=utf8
"""
版本号管理模块

分别提供用于打包的版本号，以及终端命令返回的版本号
"""
from __future__ import unicode_literals

import os


VERSION_SUFFIX_DEV = 'dev'
VERSION_SUFFIX_POST = 'post'
VERSION_SUFFIX_ALPHA = 'a'
VERSION_SUFFIX_BETA = 'b'
VERSION_SUFFIX_RC = 'rc'
VERSION_SUFFIX_NONE = None

VERSION = (1, 0, 1, VERSION_SUFFIX_POST, 0)


def get_setup_version():
    """
    获取打包使用的版本号，符合 PYPI 官方推荐的版本号方案

    :return: PYPI 打包版本号
    :rtype: str
    """
    ver = '.'.join(map(str, VERSION[:3]))

    # 若后缀描述字串为 None ，则直接返回主版本号
    if not VERSION[3]:
        return ver

    # 否则，追加版本号后缀
    hyphen = ''
    suffix = hyphen.join(map(str, VERSION[-2:]))
    if VERSION[3] in [VERSION_SUFFIX_DEV, VERSION_SUFFIX_POST]:
        hyphen = '.'
    ver = hyphen.join([ver, suffix])

    return ver


def get_cli_version():
    """
    获取终端命令版本号，若存在VERSION文件则使用其中的版本号，
    否则使用 :meth:`.get_setup_version`

    :return: 终端命令版本号
    :rtype: str
    """
    directory = os.path.dirname(os.path.abspath(__file__))
    version_path = os.path.join(directory, 'VERSION')
    if os.path.exists(version_path):
        with open(version_path) as f:
            ver = f.read()
        return ver

    return get_setup_version()
