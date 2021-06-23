# -*- coding:utf-8 -*-


from .common import copy_template_file, copy_template_folder
from .init import init_project
from .new import create_new_cases
from .ls import list_cases
from .version import print_version
from .run import run_suite


# auto load to Application cli from the following tuple
__autoload__ = (
    # generators
    init_project,
    create_new_cases,

    # routines
    print_version,
    list_cases,

    # suite/case executor
    run_suite
)

# end
