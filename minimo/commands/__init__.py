# -*- coding:utf-8 -*-


from .generators import init_project, create_new_cases, \
    copy_template_file, copy_template_folder
from .routines import print_version, list_cases
from .executors import run_suite


# auto load to Application cli from the following tuple
__autoload__ = (
    # generators
    init_project, create_new_cases,

    # routines
    print_version, list_cases,

    # executors
    run_suite
)

# end
