"""
主入口模块

用以提供终端可执行命令
"""
import os
import click

from mohand.state import env
from mohand.hand import load_hands
from mohand.version import get_cli_version


def _is_package(path):
    """
    判断传入的路径是否为一个 Python 模块包
    """
    def _exists(s):
        return os.path.exists(os.path.join(path, s))

    return (
        os.path.isdir(path) and
        (_exists('__init__.py') or _exists('__init__.pyc'))
    )


def find_mohandfile(names=None):
    """
    尝试定位 ``mohandfile`` 文件，明确指定或逐级搜索父路径

    :param str names: 可选，待查找的文件名，主要用于调试，默认使用终端传入的配置
    :return: ``mohandfile`` 文件所在的绝对路径
    :rtype: str
    """
    # 如果没有明确指定，则包含 env 中的值
    names = names or [env.mohandfile]

    # 若无 ``.py`` 扩展名，则作为待查询名称，追加到 names 末尾
    if not names[0].endswith('.py'):
        names += [names[0] + '.py']

    # name 中是否包含路径元素
    if os.path.dirname(names[0]):
        # 若存在，则扩展 Home 路径标志，并测试是否存在
        for name in names:
            expanded = os.path.expanduser(name)
            if os.path.exists(expanded):
                if name.endswith('.py') or _is_package(expanded):
                    return os.path.abspath(expanded)
    else:
        # 否则，逐级向上搜索，直到根路径
        path = '.'

        # 在到系统根路径之前停止
        while os.path.split(os.path.abspath(path))[1]:
            for name in names:
                joined = os.path.join(path, name)
                if os.path.exists(joined):
                    if name.endswith('.py') or _is_package(joined):
                        return os.path.abspath(joined)
            path = os.path.join('..', path)

    return None


def print_author(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Moore.Huang <moore@moorehy.com>')
    ctx.exit()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Version {}'.format(env.version))
    ctx.exit()


@click.group()
@click.option(
    '--mohandfile', default='mohandfile.py',
    help='被导入的 Python 模块文件')
@click.option(
    '--author', '-a', is_flag=True, callback=print_author,
    expose_value=False, is_eager=True, help='作者信息')
@click.version_option(
    version=get_cli_version(), help='版本信息')
def main(*args, **kwargs):
    """
    通用自动化处理工具
    """
    print('main:', args, kwargs)

    # 使用终端传入的 option 更新 env 中的配置值
    env.update(kwargs)


hand = load_hands()
# print('HandDict@mohand:', id(hand))


@hand._click.argument('custom', nargs=-1)
@hand._click.option('--test', default='success', help='测试附加参数')
@hand.expect(cmd='test_cmd_str', timeout=70)
def test(*args, **kwargs):
    """啦啦啦"""
    print('test:', args, kwargs)


main.add_command(test)
