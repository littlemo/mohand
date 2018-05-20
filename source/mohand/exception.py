# encoding=utf8
"""
自定义异常类
"""
from __future__ import unicode_literals


class HandDuplicationOfNameError(Exception):
    """
    Hand注册重名错误
    """

    def __init__(self, name, msg=None, *args, **kwargs):
        msg = msg or '待注册的hand名已存在: {name}'
        err = msg.format(name=name)
        super().__init__(err, *args, **kwargs)
