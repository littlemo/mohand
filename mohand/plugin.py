"""
插件的接口基类
"""
import abc
import six


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
