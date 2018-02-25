# -*- coding:utf-8 -*-
"""
    minimo.__main__

    Alias for minimo.run for the command line.
"""

import os, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if '__main__' == __name__:
    from .app import MoApplication
    MoApplication("Ratatouille", root).run()