# encoding=utf-8
"""
基础命令 options 实现
"""
from __future__ import absolute_import, unicode_literals

import os

import click
from click import ClickException, Group, Option, echo, option
from click_didyoumean import DYMMixin

import click_completion
from click_help_colors import HelpColorsCommand, HelpColorsGroup
from mohand.state import env
from mohand.vendor.prettytable import PrettyTable

CONTEXT_SETTINGS = {
    "help_option_names": ["-h", "--help"],
    "auto_envvar_prefix": "MOHAND",
}

click_completion.init()


class MohandGroup(DYMMixin, HelpColorsGroup):
    """自定义用于格式化主帮助信息的 Group 类"""
    def __init__(self, help_name_color=None, *args, **kwargs):
        self.help_name_color = help_name_color
        super(MohandGroup, self).__init__(*args, **kwargs)

    def get_help_option(self, ctx):
        # from ..core import format_help

        """Override for showing formatted main help via --help and -h options"""
        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.invoked_subcommand:
                    # legit main help
                    # echo(format_help(ctx.get_help()))
                    echo(ctx.get_help())
                else:
                    # legit sub-command help
                    echo(ctx.get_help(), color=ctx.color)
                ctx.exit()

        return Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help=u"输出帮助信息并退出",
        )


class MohandCommand(HelpColorsCommand):
    """自定义用于格式化命令帮助信息的 Command 类"""
    def __init__(self, help_name_color=None, *args, **kwargs):
        self.help_name_color = help_name_color
        super(MohandCommand, self).__init__(*args, **kwargs)

    def get_help_option(self, ctx):
        """Override for showing formatted main help via --help and -h options"""
        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.invoked_subcommand:
                    # legit main help
                    echo(ctx.get_help())
                else:
                    # legit sub-command help
                    echo(ctx.get_help(), color=ctx.color)
                ctx.exit()

        return Option(
            help_options,
            is_flag=True,
            is_eager=True,
            expose_value=False,
            callback=show_help,
            help=u"输出帮助信息并退出",
        )


def option_verbose(f):
    return option(
        '-v', '--verbose', count=True,
        expose_value=True,
        help=u'开启冗余输出')(f)


def option_author(f):
    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        echo('Moore.Huang <moore@moorehy.com>')
        ctx.exit()
    return option(
        '--author', is_flag=True, is_eager=True,
        callback=callback, expose_value=False,
        help=u'作者信息')(f)


def option_version(f):
    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        table = PrettyTable(['Package Name', 'Version'])
        table.align['Package Name'] = 'l'
        table.align['Version'] = 'l'
        for row in env.version.items():
            table.add_row(row)
        echo(table)
        ctx.exit()
    return option(
        '--version', is_flag=True, is_eager=True,
        callback=callback, expose_value=False,
        help=u'版本信息')(f)


def option_install(f):
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
            raise ClickException('%s is not supported.' % shell)

        d = os.path.dirname(path)
        if not os.path.exists(d):
            os.makedirs(d)
        f = open(path, mode)
        f.write(content)
        f.write("\n")
        f.close()

        echo('{shell} 补全插件安装完成: {path}'.format(shell=shell, path=path))
        exit(0)
    return option(
        '--install', is_flag=True, is_eager=True,
        callback=callback, expose_value=False,
        help=u"为当前 Shell 安装代码补全扩展")(f)


def option_completion(f):
    def callback(ctx, attr, value):
        if not value or ctx.resilient_parsing:
            return
        shell = click_completion.get_auto_shell()
        content = click_completion.get_code(shell=shell, prog_name="mohand")
        echo(content)
        ctx.exit()
    return option(
        '--completion', is_flag=True, is_eager=True, hidden=True,
        callback=callback, expose_value=False,
        help=u"输出当前 shell 下的代码补全脚本")(f)
