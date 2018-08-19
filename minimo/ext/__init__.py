# -*- coding:utf-8 -*-


from .generator import init_project, create_new_cases
from .commands import print_version, list_cases, run_cases


# auto load to Application cli from the following tuple
__autoload__ = (
    # generators
    init_project, create_new_cases,

    # commands
    print_version, list_cases, run_cases
)
