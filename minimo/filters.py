# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-05-22
#


import re
from .helpers import upperfirst, camelize, underscore


def convert_newline(value):
    return re.sub(r"\r\n", r"\n", value)

# end
