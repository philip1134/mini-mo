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


def _get_case_name(case_path, inst_path):
    """extract case name from case path."""

    return case_path.replace(os.path.join(
        inst_path, "cases"), "")[1:].replace("\\", "/")

# end
