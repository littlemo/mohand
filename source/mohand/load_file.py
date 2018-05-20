# encoding=utf8
from __future__ import unicode_literals

import os
import sys
import click

from mohand.state import env


def _is_package(path):
    """
    判断传入的路径是否为一个 Python 模块包

    :param str path: 待判断的路径
    :return: 返回是，则传入 path 为一个 Python 包，否则不是
    :rtype: bool
    """
    def _exists(s):
        return os.path.exists(os.path.join(path, s))

    return (
        os.path.isdir(path) and
        (_exists('__init__.py') or _exists('__init__.pyc'))
    )


def find_handfile(names=None):
    """
    尝试定位 ``handfile`` 文件，明确指定或逐级搜索父路径

    :param str names: 可选，待查找的文件名，主要用于调试，默认使用终端传入的配置
    :return: ``handfile`` 文件所在的绝对路径，默认为 None
    :rtype: str
    """
    # 如果没有明确指定，则包含 env 中的值
    names = names or [env.handfile]

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


def get_commands_from_module(imported):
    """
    从传入的 ``imported`` 中获取所有 ``click.core.Command``

    :param module imported: 导入的Python包
    :return: 包描述文档，仅含终端命令函数的对象字典
    :rtype: (str, dict(str, object))
    """
    # 如果存在 <module>.__all__ ，则遵守
    imported_vars = vars(imported)
    if "__all__" in imported_vars:
        imported_vars = [
            (name, imported_vars[name]) for name in
            imported_vars if name in imported_vars["__all__"]]
    else:
        imported_vars = imported_vars.items()

    cmd_dict = extract_commands(imported_vars)
    return imported.__doc__, cmd_dict


def is_command_object(obj):
    """
    验证传入的 obj 是否为一个 CLI 命令对象

    :param object obj: 待判断对象
    :return: 是否为 ``click.core.Command`` 命令对象
    :rtype: bool
    """
    return isinstance(obj, click.core.Command)


def extract_commands(imported_vars):
    """
    从传入的变量列表中提取命令( ``click.core.Command`` )对象

    :param dict_items imported_vars: 字典的键值条目列表
    :return: 判定为终端命令的对象字典
    :rtype: dict(str, object)
    """
    commands = dict()
    for tup in imported_vars:
        name, obj = tup
        if is_command_object(obj):
            commands.setdefault(name, obj)
    return commands


def load_handfile(path, importer=None):
    """
    导入传入的 ``handfile`` 文件路径，并返回(docstring, callables)

    也就是 handfile 包的 ``__doc__`` 属性 (字符串) 和一个 ``{'name': callable}``
    的字典，包含所有通过 mohand 的 command 测试的 callables

    :param str path: 待导入的 handfile 文件路径
    :param function importer: 可选，包导入函数，默认为 ``__import__``
    :return: 包描述文档，仅含终端命令函数的对象字典
    :rtype: (str, dict(str, object))
    """
    if importer is None:
        importer = __import__

    # 获取路径&文件名
    directory, handfile = os.path.split(path)

    # 如果路径不在 ``PYTHONPATH`` 中，则添加，以便于我们的导入正常工作
    added_to_path = False
    index = None
    if directory not in sys.path:
        sys.path.insert(0, directory)
        added_to_path = True

    # 如果路径在 ``PYTHONPATH`` 中，则临时将其移到最前，否则其他的 ``handfile``
    # 文件将会被优先导入，而不是我们想要导入的那个
    else:
        i = sys.path.index(directory)
        if i != 0:
            # 为之后的恢复保存索引号
            index = i
            # 添加到最前，然后删除原始位置
            sys.path.insert(0, directory)
            del sys.path[i + 1]

    # 执行导入（去除 .py 扩展名）
    sys_byte_code_bak = sys.dont_write_bytecode
    sys.dont_write_bytecode = True
    imported = importer(os.path.splitext(handfile)[0])
    sys.dont_write_bytecode = sys_byte_code_bak

    # 从 ``PYTHONPATH`` 中移除我们自己添加的路径
    # （仅仅出于严谨，尽量不污染 ``PYTHONPATH`` ）
    if added_to_path:
        del sys.path[0]

    # 将我们移动的 PATH 放回原处
    if index is not None:
        sys.path.insert(index + 1, directory)
        del sys.path[0]

    # 实际加载 Command
    docstring, commands = get_commands_from_module(imported)

    return docstring, commands
