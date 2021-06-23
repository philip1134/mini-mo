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
from .common import copy_template_folder
from minimo import __version__


@click.command("init")
@click.argument("name", nargs=1)
@click.option("-t", "--template", default=None,
              help=("specify project template, optional, default is 'task'"))
@click.option("-o", "--output", default=None,
              help=("generate project to the specified path"))
def init_project(name, template=None, output=None):
    """create new project from the specified template.

    usage in cli mode:

        $ mmo init [project-name] [-t template-name-or-path] [-o output-path]

    the project will be created under 'output-path', if no 'output-path'
    specified, that will be the current working directory. if not specified
    template, minimo will initialize the project with 'task' template.
    currenty template name only supports 'task', or you can specify a path
    which contains the template.

    tip: can use 'mmo' or 'minimo' as the main command after v0.4.0.

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api")

        # return True or False for `init` result
        result = mmo.call(
                        "init",
                        name="helloKitty",
                        output="./myprojects")
    """

    try:
        result = False

        project_name = camelize(name.replace("-", "_"))
        project_dir_name = underscore(project_name)

        if output is None:
            project_root_dir = os.getcwd()
        else:
            project_root_dir = os.path.abspath(output)
            if not os.path.exists(project_root_dir):
                os.makedirs(project_root_dir)

        project_dir = os.path.join(project_root_dir, project_dir_name)

        config = {
            "project_name": project_name,
            "date": time.strftime("%Y-%m-%d"),
            "version": __version__
        }

        # check out target path
        if os.path.exists(project_dir):
            error("directory '%s' already exsited" % project_dir_name)
        else:
            # check out template path
            template_dir = None
            if template:
                user_template_path = os.path.abspath(template)
                minimo_named_template_path = os.path.join(
                    ctx.minimo_root_path, "templates", "projects", template)

                if os.path.exists(user_template_path):
                    # user specified template path
                    template_dir = user_template_path
                elif os.path.exists(minimo_named_template_path):
                    # minimo provides template name
                    template_dir = minimo_named_template_path
                else:
                    # unrecognized template name
                    error("unrecognized project template: '%s'" % template)
            else:
                # use minimo default template
                template_dir = os.path.join(
                    ctx.minimo_root_path, "templates", "projects", "task")

            if template_dir is not None:
                info("create directory: %s" % project_dir_name)
                os.makedirs(project_dir)

                copy_template_folder(
                    project_dir,
                    template_dir,
                    ".mot",
                    config
                )

                result = True
    except Exception:
        result = False
    finally:
        return result


# end
