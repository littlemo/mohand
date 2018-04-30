
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
        try:
            return self[key]
        except KeyError:
            # 用以符合 __getattr__ 的特性
            raise AttributeError(key)

    def __setattr__(self, key, value):
        self[key] = value

    def first(self, *names):
        for name in names:
            value = self.get(name)
            if value:
                return value
