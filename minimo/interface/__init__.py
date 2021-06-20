# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-08-18
#


from .api import MoAPI
from .cli import MoCLI
from ..commands import __autoload__


class InterfaceFactory:
    """factory to create interface"""

    _map = {
        "api": MoAPI,
        "cli": MoCLI,
    }

    @classmethod
    def get(cls, mode, **attrs):
        """get interface instance by mode"""

        interface = cls._map.get(mode, "cli")(**attrs)

        for func in __autoload__:
            interface.add_command(func)

        return interface

# end
