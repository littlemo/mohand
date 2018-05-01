"""
装饰器

用以提供作为扩展插件开发所需的装饰器
"""
from mohand.utils import _AttributeDict
from mohand.exception import HandDuplicationOfNameError


hand = _AttributeDict({
    '_click': click,
})


def register(func):
    if hasattr(hand, func.__name__):
        raise HandDuplicationOfNameError(func.__name__)
    hand[func.__name__] = func
    return func
