# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


from .attribute_dict import SimpleAttributeDict, AttributeDict


# runtime context
class RuntimeContext(SimpleAttributeDict):
    """stores runtime context, includes application instance, callbacks,
    test suite name, minimo root path, and etc.
    """

    def __init__(self, defaults={}):
        super(RuntimeContext, self).__init__({
            "app": None,
            "counter": None,
            "reporter": None,
            "callbacks": None,
            "suite_name": None,
            "output_path": None,
            "config": AttributeDict(),
        })

# end
