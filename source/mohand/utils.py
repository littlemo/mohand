# encoding=utf8
"""
用以提供全局通用工具方法&类
"""
from __future__ import unicode_literals

from threading import RLock


class _AttributeDict(dict):
    """
    允许通过查找/赋值属性来操作键值的字典子类

    举个栗子::

        >>> m = _AttributeDict({'foo': 'bar'})
        >>> m.foo
        'bar'
        >>> m.foo = 'not bar'
        >>> m['foo']
        'not bar'

    ``_AttributeDict`` 对象还提供了一个 ``.first()`` 方法，起功能类似
    ``.get()`` ，但接受多个键名作为列表多参，并返回第一个命中的键名的值
    再举个栗子::

        >>> m = _AttributeDict({'foo': 'bar', 'biz': 'baz'})
        >>> m.first('wrong', 'incorrect', 'foo', 'biz')
        'bar'

    """

    def __getattr__(self, key):
        """重载获取属性方法，使字典支持点语法取值"""
        try:
            return self[key]
        except KeyError:
            # 用以符合 __getattr__ 的特性
            raise AttributeError(key)

    def __setattr__(self, key, value):
        """重载设置属性方法，使字典支持点语法赋值"""
        self[key] = value

    def first(self, *names):
        """返回列表key在字典中第一个不为空的值"""
        for name in names:
            value = self.get(name)
            if value:
                return value


class Singleton(type):
    """
    单例类实现(线程安全)

    .. note::

        参考实现 `singleton <https://github.com/ShichaoMa/toolkit/
        blob/master/toolkit/singleton.py>`_

    """
    lock = RLock()

    def __new__(mcs, *args, **kwargs):
        """
        元类msc通过__new__组建类对象，其中msc指Singleton

        :param list args: 可以包含类构建所需要三元素， ``类名`` ， ``父类`` ，
            ``命名空间``, 其中命名空间中 __qualname__ 和函数的 __qualname__
            均含有 classname 做为前缀，在这里，如果想替换类名，需要把以上全部替换才可以。
        :param dict kwargs: 可以自定义传递一些参数
        :return: 返回类对象,通过super(Singleton, mcs).__new__此时已经组装好了类
        :rtype: class
        """
        class_name, super_cls, dict_ = args
        dict_['_instance'] = None
        cls_ = super(Singleton, mcs).__new__(
            mcs, class_name, super_cls, dict_, **kwargs)
        return cls_

    def __call__(cls, *args, **kwargs):
        """在调用时在线程锁中实现单例实例化"""
        with cls.lock:
            cls._instance = cls._instance or \
                super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance
