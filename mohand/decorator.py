"""
装饰器

用以提供作为扩展插件开发所需的装饰器
"""
from mohand.utils import _AttributeDict


hand = _AttributeDict()


def register(func):
    hand[func.__name__] = func
    return func
