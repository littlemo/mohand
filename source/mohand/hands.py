# encoding=utf8
from __future__ import unicode_literals

import abc
import six
import click
import stevedore

from mohand.exception import HandDuplicationOfNameError
from mohand.utils import Singleton, _AttributeDict
from mohand.state import env


@six.add_metaclass(abc.ABCMeta)
class HandBase(object):
    """
    用于定义hand任务的基类
    """
    @abc.abstractmethod
    def register(self, *args, **kwargs):
        """
        注册hand任务

        :return: 返回待注册的hand函数
        :rtype: function
        """

    @abc.abstractmethod
    def version(self):
        """
        版本信息

        :return: 返回包名，版本号元组
        :rtype: (str, str)
        """


class HandDict(_AttributeDict):
    """
    Hand扩展插件集合字典(单例)
    """
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        super(HandDict, self).__init__(*args, **kwargs)
        self['_click'] = click


def load_hands():
    """
    加载hand扩展插件

    :return: 返回hand注册字典(单例)
    :rtype: HandDict
    """
    # 注册hand插件
    mgr = stevedore.ExtensionManager(
        namespace=env.plugin_namespace,
        invoke_on_load=True)

    def register_hand(ext):
        _hand = ext.obj.register()
        if hasattr(hand, _hand.__name__):
            raise HandDuplicationOfNameError(_hand.__name__)
        hand[_hand.__name__] = _hand

        _pkg, _ver = ext.obj.version()
        env.version[_pkg] = _ver

    mgr.map(register_hand)
    return hand


#: 所有已注册hand插件的装饰器集合实例，可通过 ``.`` 语法获取
hand = HandDict()
