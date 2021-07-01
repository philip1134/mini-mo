# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#


import os
import time
import click
from ..utils import *
from ..globals import ctx
from .common import copy_template_folder, verify_root_path


@click.command("new")
@click.argument("cases", nargs=-1)
@click.option("--author", "-a", nargs=1, type=click.STRING)
def create_new_cases(cases, author=None):
    """generate case from templates.

    usage in cli mode:

        $ mmo new [cases...] [-a author]

    for example:

        $ mmo new suite1/case1 suite2/case2 case3 [-a hellokitty]

    minimo will walk through the sub-directory of task suite, if templates
    exists in task suite, it initializes the case by the suite specified
    templates, otherwise, by the project default templates.

    if specified author name, it will be filled in the template file, or minimo
    will get the current system user as the author name.

    tip: can use 'mmo' or 'minimo' as the main command after v0.4.0.

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api",
                    root_path=instance_project_path)

        # return successfully created cases list
        cases = mmo.call(
                    "new",
                    cases=["case1", "suite2/case1", "suite2/case2"])

    """

    try:
        success_cases = []

        if not verify_root_path(ctx):
            return success_cases

        stage("prepare to create case...")

        if author is None:
            import getpass
            author = getpass.getuser()

        config = {
            "author": author,
            "date": time.strftime("%Y-%m-%d")
        }

        for case in set(cases):
            # checking templates
            dirs = ["cases"] + case.split("/")
            template_dir = None
            while len(dirs) > 0:
                dirs.pop()
                _templatedir = os.path.join(ctx.app.inst_path,
                                            *(dirs + ["templates"]))
                if os.path.exists(_templatedir):
                    template_dir = _templatedir
                    break

            if template_dir is None:
                warning(
                    "no template found, abort creating task under cases/%s" %
                    case)
            else:
                # checking target path
                target = os.path.join(ctx.app.inst_path, "cases", case)
                if os.path.exists(target):
                    warning(
                        "directory cases/%s already existed, skip this step!" %
                        case)
                    continue
                else:
                    info("create directory: cases/%s" % case)
                    os.makedirs(target)

                info("create case by project template %s" % (
                    template_dir.replace(ctx.app.inst_path,
                                         "%s.root" % ctx.app.name)))

                # copy files
                config["case_name"] = re.sub(r"\W+", ".", case)
                copy_template_folder(target, template_dir, ".mako", config)
                success_cases.append(case)

                stage("case created under %s.root/cases" % ctx.app.name)
    except Exception:
        pass
    finally:
        return success_cases


# end
