# encoding=utf8
"""
此模块提供随包附带的基础 ``hand`` ，用以实现最基础功能，即将 ``handfile``
中的目标方法装饰为一个 ``mohand`` 子命令的 ``general`` 装饰器，更多扩展
``hand`` 您可以通过安装扩展包来获得
"""
import logging
from mohand.hands import hand

log = logging.getLogger(__name__)


def _register(func):
    """
    将被装饰函数注册到 hand 单例字典中

    :param object func: 被装饰函数
    :return: 被装饰的函数本身（不进行封装）
    :rtype: function
    """
    hand[func.__name__] = func
    return func


@_register
def general(*dargs, **dkwargs):
    """
    将被装饰函数封装为一个 :class:`click.core.Command` 类，
    此装饰器并不提供额外的复杂功能，仅提供将被装饰方法注册为一个 ``mohand`` 子命令的功能

    该装饰器作为一个一般装饰器使用（如： ``@hand.general`` ）

    .. note::

        该装饰器会在插件系统加载外部插件前辈注册到 :data:`.hands.hand` 中。

        此处的 ``general`` 装饰器同时兼容有参和无参调用方式

    :param int log_level: 当前子命令的日志输出等级，默认为： ``logging.INFO``
    :return: 被封装后的函数
    :rtype: function
    """
    invoked = bool(len(dargs) == 1 and not dkwargs and callable(dargs[0]))
    if invoked:
        func = dargs[0]

    def wrapper(func):
        @hand._click.command(
            name=func.__name__.lower(),
            help=func.__doc__)
        def _wrapper(*args, **kwargs):
            log_level = dkwargs.pop('log_level', logging.INFO)
            log.setLevel(log_level)

            log.debug("decrator param: {} {}".format(dargs, dkwargs))
            log.debug("function param: {} {}".format(args, kwargs))

            func(*args, **kwargs)
        return _wrapper
    return wrapper if not invoked else wrapper(func)
