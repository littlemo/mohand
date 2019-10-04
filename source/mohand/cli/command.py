# encoding=utf8
"""
主入口模块

用以提供终端可执行命令，并注册子命令
"""
from __future__ import absolute_import, unicode_literals

import logging
import sys

from mohand import hands, options
from mohand.load_file import find_handfile, load_handfile
from mohand.state import env

import six
import click

if six.PY2:
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


@click.group(invoke_without_command=True)
@options.author_option
@options.version_option
@options.install_cb_option
@options.completion_cb_option
@click.pass_context
def cli(ctx, *args, **kwargs):
    """
    通用自动化处理工具

    详情参考 `GitHub <https://github.com/littlemo/mohand>`_
    """
    log.debug('cli: {} {}'.format(args, kwargs))

    # 使用终端传入的 option 更新 env 中的配置值
    env.update(kwargs)

    if ctx.invoked_subcommand is None:
        # Display help to user, if no commands were passed.
        click.echo(ctx.get_help())


# 将从 handfile 文件中加载到的 Command 注册到 cli 中
for cmd in commands.values():
    cli.add_command(cmd)

log.debug('加载完毕，并注册子命令: {}'.format(
    [c.name for c in commands.values()]))
