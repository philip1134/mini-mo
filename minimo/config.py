# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-25
#

class Config(dict):
    """Works like dict but provides methods to get attribute by '.',
    such as:
        config = Config({'foo': foo, 'bar': bar})
        print config.foo
        config.bar = bar2
    """
    
    def __init__(self, defaults = {}):
        dict.__init__(self, defaults)

    def __getattr__(self, attrname):  
        return self[attrname]

    def __setattr__(self, attrname, value):
        self[attrname] = value