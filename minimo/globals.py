# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#


import os
from .attribute_dict import SimpleAttributeDict, AttributeDict
from .counter import Counter


# constants
BLOCK_SPLITTER = "=" * 50
SECTION_SPLITTER = "-" * 50


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


ctx = RuntimeContext()
ctx.counter = Counter()
ctx.minimo_root_path = os.path.dirname(__file__)

# end
