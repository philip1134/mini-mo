# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#


import os
import time
import shutil
from mako.template import Template
from ..helpers import *
from ..globals import g, MINIMO_ROOT
from ..route import register
from minimo import __version__


__template_hooks = {
    "vue-webpack": "vue init webpack {}",
    "vue-webpack-simple": "vue init webpack-simple {}"
}

@register("init", "help.init", True)
def minimo_generate_project(args = {}):
    """initialize project from templates"""

    for project_name in args["args"]:
        project_name = camelize(project_name.replace("-", "_"))
        project_dir_name = underscore(project_name)
        project_dir = os.path.join(os.getcwd(), project_dir_name)

        if "s" in args:
            project_abbreviation = args["s"].upper()
        else:
            project_abbreviation = project_name[:3].upper()

        config = {
            "project_name": project_name,
            "project_abbreviation": project_abbreviation,
            "date": time.strftime("%Y-%m-%d"),
            "version": __version__
        }

        # check out target path
        if os.path.exists(project_dir):
            warning(_("warning.directory_existed"), project_dir_name)
        else:
            # check out template path
            template_dir = None
            if "t" in args:
                user_template_path = os.path.join(os.getcwd(), args["t"])
                minimo_named_template_path = os.path.join(\
                    MINIMO_ROOT, "templates", args["t"], "project")

                if os.path.exists(user_template_path):
                    # user specified template path
                    template_dir = user_template_path
                elif os.path.exists(minimo_named_template_path):
                    # minimo provides template name
                    template_dir = minimo_named_template_path
                else:
                    # unrecognized template name
                    error(_("error.unrecognized_project_template"), args["t"])
            else:
                # use minimo default template
                template_dir = os.path.join(\
                    MINIMO_ROOT, "templates", "task", "project")

            if template_dir is not None:
                info(_("info.create_dir"), project_dir_name)
                os.makedirs(project_dir)

                copy_template_folder(project_dir, template_dir, ".mot", config)


def copy_template_file(
    dest,
    src,
    config = {}
):
    """copy template file from src to dest, replace the placeholder in template
    file by the given config keywords."""

    try:
        if os.path.exists(dest):
            warning(_("warning.file_existed"))
            return False

        content = Template(
            filename=src,
            default_filters=["trim"],
            output_encoding="utf-8"
        ).render(**config)

        with open(dest, "w") as f:
            f.write(content)

        info(_("info.create_file"), os.path.basename(dest))

        return True
    except:
        error(_("error.fail_to_create_file"),
            os.path.basename(dest), format_traceback())
        return False


def copy_template_folder(
    dest_dir,
    template_dir,
    template_file_suffix,
    config
):
    """copy template directory to dest"""

    for dirpath, dirs, files in os.walk(template_dir):
        dest_subdir_name = os.path.relpath(dirpath, template_dir)
        dest_subdir = os.path.join(dest_dir, dest_subdir_name)

        if "." != dest_subdir_name:
            if os.path.exists(dest_subdir):
                info(_("info.directory_existed"), dest_subdir_name)
            else:
                info(_("info.create_dir"), dest_subdir_name)
                os.makedirs(dest_subdir)

        for file in [f for f in files if _files_filter(f)]:
            src = os.path.join(dirpath, file)
            if os.path.splitext(file)[-1] == template_file_suffix:
                # copy template file
                fparts = file.rpartition(template_file_suffix)
                dst = os.path.join(dest_subdir, "".join([fparts[0], fparts[2]]))
                copy_template_file(dst, src, config)
            else:
                # copy raw file
                dst = os.path.join(dest_subdir, file)
                shutil.copyfile(src, dst)
                info(_("info.create_file"), os.path.basename(dst))


def _files_filter(name):
    """filter file names out."""

    return not name.lower().endswith((
        ".pyc",
        ".pyo",
        ".placeholder"
    ))

# end
