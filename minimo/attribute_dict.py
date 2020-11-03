# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-25
#


import copy


class AttributeDict(dict):
    """Works like dict but provides methods to get attribute by '.'.

    such as::
        attrDict = AttributeDict({'foo': foo, 'bar': bar})
        print(attrDict.foo)
        attrDict.bar = bar2
    """

    def __init__(self, defaults={}):
        super(AttributeDict, self).__init__(defaults)
        # dict.__init__(self, defaults)

    def __getattr__(self, attrname):
        return self.get(attrname)

    def __setattr__(self, attrname, value):
        self[attrname] = value

    def __deepcopy__(self, memo):
        return AttributeDict(copy.deepcopy(self.copy(), memo))

# end
