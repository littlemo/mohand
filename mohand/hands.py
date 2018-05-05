import abc
import six
import click
import stevedore

from mohand.exception import HandDuplicationOfNameError
from mohand.utils import Singleton, _AttributeDict


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


class HandDict(_AttributeDict):
    """
    Hand扩展插件集合字典(单例)
    """
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['_click'] = click


def load_hands():
    """
    加载hand扩展插件

    :return: 返回hand注册字典(单例)
    :rtype: HandDict
    """
    handdict = HandDict()

    # 注册hand插件
    mgr = stevedore.ExtensionManager(
        namespace='mohand.plugin.hand',
        invoke_on_load=True)

    def register_hand(ext):
        _hand = ext.obj.register()
        if hasattr(handdict, _hand.__name__):
            raise HandDuplicationOfNameError(_hand.__name__)
        handdict[_hand.__name__] = _hand
        # print('register hand:', _hand.__name__)

    mgr.map(register_hand)
    # print('HandDict@mohand:', handdict)
    # print('HandDict@mohand:', id(handdict))

    return handdict


class Hand(object):
    """
    希望被提取为 MoHand 的 hand 的抽象基类

    其子类的实例将被作为合法的 hand 从 handfile 中被 ``mohand`` 工具加载

    对于如何使用 `~mohand.hands.Hand` 子类，可查看相关文档
    """
    def __init__(self, name=None, *args, **kwargs):
        self.name = name or 'undefined'

    def run(self):
        raise NotImplementedError


class WrappedCallableHand(Hand):
    """
    透明封装一个传入的 ``callable_`` ，并将其标记为一个有效的 hand 。

    通常通过一个扩展插件实现的相应功能的装饰器来使用，而非直接使用
    """
    def __init__(self, callable_, *args, **kwargs):
        super(WrappedCallableHand, self).__init__(*args, **kwargs)
        self.wrapped = callable_

        if hasattr(callable_, '__name__'):
            if self.name == 'undefined':
                self.__name__ = self.name = callable_.__name__
            else:
                self.__name__ = self.name
        if hasattr(callable_, '__doc__'):
            self.__doc__ = callable_.__doc__
        if hasattr(callable_, '__module__'):
            self.__module__ = callable_.__module__

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        return self.wrapped(*args, **kwargs)

    def __getattr__(self, k):
        return getattr(self.wrapped, k)


hand = HandDict()
