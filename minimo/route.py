# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-27
#

from functools import wraps
from .globals import g

g.routes = {}
def register(cmd, help = ""):
    """bind command to callback."""
    def decorator(f):
        @wraps(f)
        def decorated_func(*args, **kwargs):
            return f(*args, **kwargs)
        g.routes[cmd] = {
            "handler": f,
            "help": help
        }
        return decorated_func
    return decorator