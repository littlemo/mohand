import stevedore

from mohand.hand import HandDict
from mohand.exception import HandDuplicationOfNameError


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
