# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#


import os
import time
import click
import shutil
from mako.template import Template
from ..helpers import *
from ..globals import ctx
from ..filters import convert_newline
from minimo import __version__


@click.command("init")
@click.argument("name", nargs=1)
@click.option("-t", "--template", default=None,
              help=("specify project template, optional, default is 'task'"))
def init_project(name, template):
    """create new project from the specified template.

    usage:

        $ mmo init [project-name] [-t template-name-or-path]

    the project will be created under current working directory. if not
    specified template, minimo will initialized the project with 'task'
    template. currenty template name only supports 'task', or you can
    specify a path which contains the template.

    tip: can use 'mmo' or 'minimo' as the main command after v0.4.0.
    """

    project_name = camelize(name.replace("-", "_"))
    project_dir_name = underscore(project_name)
    project_dir = os.path.join(os.getcwd(), project_dir_name)

    config = {
        "project_name": project_name,
        "date": time.strftime("%Y-%m-%d"),
        "version": __version__
    }

    # check out target path
    if os.path.exists(project_dir):
        warning("directory '%s' already exsited" % project_dir_name)
    else:
        # check out template path
        template_dir = None
        if template:
            # user_template_path = os.path.join(os.getcwd(), template)
            user_template_path = os.path.abspath(template)
            minimo_named_template_path = os.path.join(
                ctx.minimo_root_path, "templates", template, "project")

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
                ctx.minimo_root_path, "templates", "task", "project")

        if template_dir is not None:
            info("create directory: %s" % project_dir_name)
            os.makedirs(project_dir)

            copy_template_folder(project_dir, template_dir, ".mot", config)


@click.command("new")
@click.argument("cases", nargs=-1)
@click.option("--author", "-a", nargs=1, type=click.STRING)
def create_new_cases(cases, author):
    """generate case from templates.

    usage:

        $ mmo new [cases...] [-a author]

    for example:

        $ mmo new suite1/case1 suite2/case2 case3 [-a hellokitty]

    minimo will walk through the sub-directory of task suite, if templates
    exists in task suite, it initializes the case by the suite specified
    templates, otherwise, by the project default templates.

    if specified author name, it will be filled in the template file, or minimo
    will get the current system user as the author name.

    tip: can use 'mmo' or 'minimo' as the main command after v0.4.0.
    """

    if ctx.app.root_path is None:
        error('not in minimo project root folder')
        return

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
            _templatedir = os.path.join(ctx.app.root_path,
                                        *(dirs + ["templates"]))
            if os.path.exists(_templatedir):
                template_dir = _templatedir
                break

        if template_dir is None:
            warning(
                "no template found, abort creating task under cases/%s" % case)
        else:
            # checking target path
            target = os.path.join(ctx.app.root_path, "cases", case)
            if os.path.exists(target):
                warning(
                    "directory cases/%s already existed, skip this step!" %
                    case)
                continue
            else:
                info("create directory: cases/%s" % case)
                os.makedirs(target)

            info("create case by project template %s" % (
                template_dir.replace(ctx.app.root_path,
                                     "%s.root" % ctx.app.name)))

            # copy files
            config["case_name"] = os.path.basename(case)
            copy_template_folder(target, template_dir, ".mako", config)

            stage("case created under %s.root/cases" % ctx.app.name)


def copy_template_file(
    dest,
    src,
    config={}
):
    """copy template file from src to dest, replace the placeholder in template
    file by the given config keywords."""

    try:
        if os.path.exists(dest):
            warning("file already existed, skip this step.")
            return False

        content = Template(
            filename=src,
            default_filters=["trim"],
            output_encoding="utf-8"
        ).render(**config)

        with open(dest, "w") as f:
            f.write(convert_newline(content))

        info("\tcreate file: %s" % os.path.basename(dest))

        return True
    except Exception:
        error("fail to create file %s!\nreason:\n%s" % (
            os.path.basename(dest),
            format_traceback()))
        return False


def copy_template_folder(
    dest_dir,
    template_dir,
    template_file_suffix,
    config
):
    """copy template directory to dest."""

    for dirpath, dirs, files in os.walk(template_dir):
        dest_subdir_name = os.path.relpath(dirpath, template_dir)
        dest_subdir = os.path.join(dest_dir, dest_subdir_name)

        if "." != dest_subdir_name:
            if os.path.exists(dest_subdir):
                info("directory %s already exsited" % dest_subdir_name)
            else:
                info("create directory: %s" % dest_subdir_name)
                os.makedirs(dest_subdir)

        for file in [f for f in files if _files_filter(f)]:
            src = os.path.join(dirpath, file)
            if os.path.splitext(file)[-1] == template_file_suffix:
                # copy template file
                fparts = file.rpartition(template_file_suffix)
                dst = os.path.join(dest_subdir, "".join(
                    [fparts[0], fparts[2]]))
                copy_template_file(dst, src, config)
            else:
                # copy raw file
                dst = os.path.join(dest_subdir, file)
                shutil.copyfile(src, dst)
                info("\tcreate file: %s" % os.path.basename(dst))


def _files_filter(name):
    """filter file names out."""

    return not name.lower().endswith((
        ".pyc",
        ".pyo",
        ".placeholder"
    ))

# end
