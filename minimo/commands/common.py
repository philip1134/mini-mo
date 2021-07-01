# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


import os
import shutil
from ..utils import *
from mako.template import Template


def verify_root_path(context):
    """check out project instance path was set or not"""

    if context.app.inst_path is None:
        error('not in minimo project root folder')
        return False
    else:
        return True


def get_case_name(case_path, inst_path):
    """extract case name from case path."""

    return case_path.replace(os.path.join(
        inst_path, "cases"), "")[1:].replace("\\", "/")


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
        ).render_unicode(**config)

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
