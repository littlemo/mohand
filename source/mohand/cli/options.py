# encoding=utf-8
"""
基础命令 options 实现
"""
from __future__ import absolute_import, unicode_literals

import os

import click
import click_completion
from mohand.state import env
from mohand.vendor.prettytable import PrettyTable

click_completion.init()


def author_option(f):
    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        click.echo('Moore.Huang <moore@moorehy.com>')
        ctx.exit()
    return click.option(
        '--author', is_flag=True, is_eager=True,
        callback=callback, expose_value=False,
        help='作者信息')(f)


def version_option(f):
    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        table = PrettyTable(['Package Name', 'Version'])
        table.align['Package Name'] = 'l'
        table.align['Version'] = 'l'
        for row in env.version.items():
            table.add_row(row)
        click.echo(table)
        ctx.exit()
    return click.option(
        '--version', is_flag=True, is_eager=True,
        callback=callback, expose_value=False,
        help='版本信息')(f)


def install_cb_option(f):
    def callback(ctx, attr, value):
        if not value or ctx.resilient_parsing:
            return value

        prog_name = click.get_current_context().find_root().info_name
        shell = click_completion.get_auto_shell()
        mode = path = None

        if shell == 'fish':
            path = path or os.path.expanduser('~') + '/.config/fish/completions/%s.fish' % prog_name
            mode = mode or 'w'
            content = 'eval (mohand --completion)'
        elif shell == 'bash':
            path = path or os.path.expanduser('~') + '/.bash_completion'
            mode = mode or 'a'
            content = 'eval "$(mohand --completion)"'
        elif shell == 'zsh':
            path = path or os.path.expanduser('~') + '/.zshrc'
            mode = mode or 'a'
            content = 'eval "$(mohand --completion)"'
        else:
            raise click.ClickException('%s is not supported.' % shell)

        d = os.path.dirname(path)
        if not os.path.exists(d):
            os.makedirs(d)
        f = open(path, mode)
        f.write(content)
        f.write("\n")
        f.close()

        click.echo('{shell} 补全插件安装完成: {path}'.format(shell=shell, path=path))
        exit(0)
    return click.option(
        '--install', is_flag=True, is_eager=True,
        callback=callback, expose_value=False,
        help="为当前 Shell 安装代码补全扩展")(f)


def completion_cb_option(f):
    def callback(ctx, attr, value):
        if not value or ctx.resilient_parsing:
            return
        shell = click_completion.get_auto_shell()
        content = click_completion.get_code(shell=shell, prog_name="mohand")
        click.echo(content)
        ctx.exit()
    return click.option(
        '--completion', is_flag=True, is_eager=True, hidden=True,
        callback=callback, expose_value=False,
        help="输出当前 shell 下的代码补全脚本")(f)
