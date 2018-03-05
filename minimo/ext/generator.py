# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import os
import time
from string import Template
from ..helpers import *
from ..globals import *
from ..route import register

@register("init", "help.init", True)
def minimo_generate_project(args = {}):
    """initialize project from templates"""

    for project_name in args["args"]:
        project_name = project_name.replace("-", "_")
        project_name_camelized = camelize(project_name)
        project_dir_name = underscore(project_name)
        project_dir = os.path.join(os.getcwd(), project_dir_name)
        config = {
            "project_name": project_name_camelized,
            "date": time.strftime("%Y-%m-%d")
        }

        # checking target path
        if os.path.exists(project_dir):
            warning(_("warning.abort_creating_dir_for_existence"), project_dir_name)
        else:
            # check out template path
            template_dir = None
            if args.has_key("t"):
                user_template_path = os.path.join(os.getcwd(), args["t"])
                minimo_named_template_path = os.path.join(\
                    os.path.dirname(__file__), "..", "templates", args["t"])

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
                    os.path.dirname(__file__), "..", "templates", "default")

            if template_dir is not None:
                info(_("info.create_dir"), project_dir_name)
                os.makedirs(project_dir)
                
                _copy_template_dir(project_dir, template_dir, ".mot", config)

@register("new", "help.new", True)
def minimo_generate_cases(args = {}):
    """generate case from templates. it will walk through the sub-directory of task suite,
    if templates exists in task suite, it initializes the case by the suite specified templates,
    otherwise, by the project default templates."""

    if g.app.root_path is None:
        error(_("error.invalid_minimo_project_directory"))
        return

    if not validate_keys(args, {"a": _("error.case_author_name_required")}):
        return

    info(_("info.prepare_to_create_case"))

    date = time.strftime("%Y-%m-%d")
    config = {
        "author": args["a"],
        "date": date
    }
    for case in set(args["args"]):
        # checking templates
        dirs = ["cases"] + case.split("/")
        template_dir = None
        while len(dirs) > 0:
            dirs.pop()
            _templatedir = os.path.join(g.app.root_path, *(dirs + ["templates"]))
            if os.path.exists(_templatedir):
                template_dir = _templatedir
                break                    
            
        if template_dir is None:
            warning(_("warning.abort_creating_case_for_no_template"), case)
        else:
            # checking target path
            target = os.path.join(g.app.root_path, "cases", case)
            if os.path.exists(target):
                warning(_("warning.abort_creating_case_for_existence"), case)
                continue
            else:
                info(_("info.creating_case_dir"), case)
                os.makedirs(target)

            info(_("info.creating_case_by_template"), \
                template_dir.replace(g.app.root_path, "%s.root"%g.app.name))
            
            # copy files
            config["case_name"] = os.path.basename(case)
            _copy_template_dir(target, template_dir, ".template", config)
            
            info(_("info.case_created"), g.app.name)

def _copy_template_file(dest, src, config = {}):
    """copy template file from src to dest, replace the placeholder in template file
    by the given config keywords."""

    try: 
        with open(src, "r") as src_file:
            content = Template(src_file.read())
           
        content = content.safe_substitute(**config)
        f = open(dest, "w")
        f.write(content)
        f.close()

        info(_("info.create_file"), os.path.basename(dest))
    except:
        error(_("error.fail_to_create_file"), os.path.basename(dest), format_traceback())

def _copy_template_dir(dest_dir, template_dir, template_file_afterfix, config):
    """copy template directory to dest"""

    for dirpath, dirs, files in os.walk(template_dir):
        dest_subdir_name = os.path.relpath(dirpath, template_dir)
        dest_subdir = os.path.join(dest_dir, dest_subdir_name)

        if "." != dest_subdir_name:
            if os.path.exists(dest_subdir):
                info(_("info.skip_creating_dir_for_existence"), dest_subdir_name)
            else:
                info(_("info.create_dir"), dest_subdir_name)
                os.makedirs(dest_subdir)

        if ".placeholder" in files:
            files.remove(".placeholder")
            
        for file in files:
            _copy_template_file(
                os.path.join(dest_subdir, file.replace(template_file_afterfix, "")), 
                os.path.join(dirpath, file), 
                config)
