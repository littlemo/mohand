import click
from mohand.utils import Singleton, _AttributeDict


class HandDict(_AttributeDict):
    """
    Hand数据字典(单例)
    """
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self['_click'] = click
