# -*- coding:utf-8 -*-
"""
    minimo.__main__

    Alias for minimo.run for the command line.
"""

if "__main__" == __name__:
    from .app import MoApplication
    MoApplication().run()