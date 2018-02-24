#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os, sys
reload(sys)
sys.setdefaultencoding('utf-8')

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if '__main__' == __name__:
    from .app import MoApplication
    MoApp("Ratatouille", root).run()