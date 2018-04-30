"""
版本号管理模块

分别提供用于打包的版本号，以及终端命令返回的版本号
"""
VERSION_SUFFIX_DEV = 'dev'
VERSION_SUFFIX_POST = 'post'
VERSION_SUFFIX_ALPHA = 'a'
VERSION_SUFFIX_BETA = 'b'
VERSION_SUFFIX_RC = 'rc'
VERSION_SUFFIX_NONE = None

VERSION = (0, 0, 0, VERSION_SUFFIX_DEV, 0)


def get_setup_version():
    """
    获取打包使用的版本号，符合 PYPI 官方推荐的版本号方案
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
