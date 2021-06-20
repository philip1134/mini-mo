# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


import os


def get_case_name(case_path, inst_path):
    """extract case name from case path."""

    return case_path.replace(os.path.join(
        inst_path, "cases"), "")[1:].replace("\\", "/")

# end
