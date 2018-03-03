# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-27
#

import collections
from functools import wraps
from .globals import g

g.routes = collections.OrderedDict()

def register(cmd, help = "", trans = False):
    """register command to minimo application interface."""

    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            return f(*args, **kwargs)
        g.routes[cmd] = {
            "handler": f.__name__,
            "help": help,
            "trans": trans
        }
        return decorated_func
    return decorator