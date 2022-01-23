# -*- coding:utf-8 -*-


from minimo.commands.init import init_project
from minimo.commands.new import create_new_cases
from minimo.commands.ls import list_cases
from minimo.commands.version import print_version
from minimo.commands.run import run_suite
from minimo.commands.start import start_scheduler


# auto load to Application cli from the following tuple
__autoload__ = [
    # generators
    init_project,
    create_new_cases,

    # routines
    print_version,
    list_cases,

    # suite/case executor
    run_suite,

    # scheduler
    start_scheduler
]


# end
