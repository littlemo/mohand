# encoding=utf8
"""
主入口模块

用以提供终端可执行命令，并注册子命令
"""
from __future__ import unicode_literals

import sys
import click
import logging

from prettytable import PrettyTable

from mohand import hands
from mohand.state import env
from mohand.load_file import find_handfile, load_handfile

if sys.version > '3':
    PY3 = True
else:
    PY3 = False

if PY3:
    from imp import reload

if not PY3:
    reload(sys)
    sys.setdefaultencoding('utf8')

click.disable_unicode_literals_warning = True

LOG_FORMAT = "[%(asctime)s][%(name)s:%(lineno)s][%(levelname)s] %(message)s"
logging.basicConfig(
    level=logging.WARN,
    format=LOG_FORMAT,
    stream=sys.stdout,
)
log = logging.getLogger(__name__)


def print_author(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Moore.Huang <moore@moorehy.com>')
    ctx.exit()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    table = PrettyTable(['Package Name', 'Version'])
    table.align['Package Name'] = 'l'
    table.align['Version'] = 'l'
    for row in env.version.items():
        table.add_row(row)
    click.echo(table)
    ctx.exit()


# 加载所有扩展 hand
hands.load_hands()
log.debug('hand@mohand: {}'.format(hands.hand))

# 获取 handfile 文件路径
handfile = find_handfile()
if not handfile:
    click.echo('[{}] {}'.format(
        click.style('ERROR', bg='red'),
        '未找到 handfile 文件！'))
    sys.exit(1)
log.info('handfile => {}'.format(handfile))

# 加载 handfile 文件
handfile_doc, commands = load_handfile(handfile)
log.info('handfile文档: {}'.format(handfile_doc))


@click.group()
@click.option(
    '--author', is_flag=True, callback=print_author,
    expose_value=False, is_eager=True, help='作者信息')
@click.option(
    '--version', is_flag=True, callback=print_version,
    expose_value=False, is_eager=True, help='版本信息')
def cli(*args, **kwargs):
    """
    通用自动化处理工具

    详情参考 `GitHub <https://github.com/littlemo/mohand>`_
    """
    log.debug('cli: {} {}'.format(args, kwargs))

    # 使用终端传入的 option 更新 env 中的配置值
    env.update(kwargs)


# 将从 handfile 文件中加载到的 Command 注册到 cli 中
for cmd in commands.values():
    cli.add_command(cmd)

log.debug('加载完毕，并注册子命令: {}'.format(
    [c.name for c in commands.values()]))
