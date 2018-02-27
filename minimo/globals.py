# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#

from .config import Config

# constants
BLOCK_SPLITTER = "=" * 50
SECTION_SPLITTER = "-" * 50

# globals
g = Config({
    "app": None, 
    "callbacks": None, 
    "line": 1,
    "task_suite": None,
    "errors": []
})

def report_exception(point, reason = ""):
    g.errors.append(_("info.report_case_exception").format(point, reason))
