# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import os
import click
import fnmatch
from ..utils import *
from ..globals import ctx
from .common import get_case_name, verify_root_path


@click.command("ls")
@click.argument("patterns", nargs=-1)
def list_cases(patterns=[]):
    """list all standard task cases.

    usage in cli mode:

        $ mmo ls [pattern...]

    "pattern" supports Unix shell-style wildcards, such as * or ?.
    if not specified "pattern", it will list all standard cases' names under
    "cases" folder. if specified "pattern", it will search the case name by
    "pattern". can give multiple patterns, such as：

        $ mmo ls foo bar*

    tip: can use 'mmo' or 'minimo' as the main command after v0.4.0.

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api",
                    root_path=instance_project_path)

        # return sorted valid cases
        sorted_cases = mmo.call("ls")
    """

    if not verify_root_path(ctx):
        return []

    cases = []
    pattern = "|".join([fnmatch.translate(ptn) for ptn in patterns])

    # loop for standard case
    case_dir = os.path.join(ctx.app.inst_path, "cases")
    for _root, _dirs, _files in os.walk(case_dir):
        if "__main__.py" in _files:
            _name = get_case_name(_root, ctx.app.inst_path)
            if pattern:
                if re.match(pattern, _name):
                    cases.append(_name)
            else:
                cases.append(_name)

    result = sorted(cases)
    info("\n".join(result))
    stage("totally %d" % len(result))

    return result


# end
