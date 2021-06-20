# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#


import os
from .counter import Counter
from .runtime_context import RuntimeContext


# constants
BLOCK_SPLITTER = "=" * 50
SECTION_SPLITTER = "-" * 50


# runtime context
ctx = RuntimeContext()
ctx.counter = Counter()
ctx.minimo_root_path = os.path.dirname(__file__)

# end
