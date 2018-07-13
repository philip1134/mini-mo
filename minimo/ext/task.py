# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import os
import sys
import re
import time
import runpy
import subprocess
import collections
from ..globals import *
from ..helpers import *
from ..route import register
from generator import copy_template_file, copy_template_folder


@register("new", "help.task.new", True, "task")
def task_generate_cases(args = {}):
    """generate case from templates. it will walk through the sub-directory
    of task suite, if templates exists in task suite, it initializes the case
    by the suite specified templates, otherwise, by the project default
    templates."""

    if g.app.root_path is None:
        error(_("error.invalid_minimo_project_directory"))
        return

    if not validate_keys(args,
        {"a": _("error.author_name_required")}):
        return

    info(_("info.task.prepare_to_create_case"))

    config = {
        "author": args["a"],
        "date": time.strftime("%Y-%m-%d")
    }
    for case in set(args["args"]):
        # checking templates
        dirs = ["cases"] + case.split("/")
        template_dir = None
        while len(dirs) > 0:
            dirs.pop()
            _templatedir = os.path.join(g.app.root_path,
                *(dirs + ["templates"]))
            if os.path.exists(_templatedir):
                template_dir = _templatedir
                break

        if template_dir is None:
            warning(_("warning.task.no_template"), case)
        else:
            # checking target path
            target = os.path.join(g.app.root_path, "cases", case)
            if os.path.exists(target):
                warning(_("warning.task.case_existed"),
                    case)
                continue
            else:
                info(_("info.task.creating_case_dir"), case)
                os.makedirs(target)

            info(_("info.task.creating_case_by_template"),
                template_dir.replace(g.app.root_path, "%s.root"%g.app.name))

            # copy files
            config["case_name"] = os.path.basename(case)
            copy_template_folder(target, template_dir, ".mako", config)

            info(_("info.task.case_created"), g.app.name)


@register("run", "help.task.run", True, "task")
def task_run_cases(args = {}):
    """run task cases"""

    tasks = collections.OrderedDict()
    task_suite = "task"

    # check case runner
    for case in set(args["args"]):
        runner_path = os.path.join(g.app.root_path, "cases", case)
        task_suite = "{0}_{1}".format(task_suite, case.replace("/", "_"))

        # loop for __main__.py
        valid_case = False
        for _root, _dirs, _files in os.walk(runner_path):
            if "__main__.py" in _files:
                _name = _root.replace(\
                    os.path.join(g.app.root_path, "cases"), "")[1:]\
                    .replace("\\", "/")
                valid_case = True
                if _name not in tasks:
                    tasks[_name] = _root
                    info(_("info.task.add_task"), _name)

        if not valid_case:
            warning(_("warning.task.not_standard_case"), case, g.app.name)
            report_exception(case, _("info.task.not_standard_case"))

    g.task_suite = "{0}_{1}".format(task_suite,
        time.strftime("%Y_%m_%d_%H_%M_%S"))

    if "concorrence" == g.app.run_cases and "s" not in args:
        _run_cases_concorrence(tasks)
    else:
        _run_cases_serial(tasks)

    info(_("info.task.report_mission_complete"),
        BLOCK_SPLITTER, len(tasks), len(g.errors))
    if len(g.errors) > 0:
        info(_("info.task.failed_tasks"), "\nx ".join(g.errors))


def _run_cases_serial(tasks = {}):
    """serial type to run cases"""

    for _name, _path in tasks.items():
        try:
            info(_("info.task.executing_task"), _name)
            module_path = os.path.abspath(os.path.join(_path, ".."))
            if module_path not in sys.path:
                sys.path.insert(0, module_path)

            runpy.run_path(_path)
        except:
            report_exception(_name, format_traceback())
            error(_("error.task.exception_in_case"), _name)


def _run_cases_concorrence(tasks = {}):
    """concorrence type to run cases"""

    sp = []
    for _name, _path in tasks.items():
        try:
            info(_("info.task.executing_task"), _name)
            sp_env = os.environ.copy()
            sp_env['PYTHONPATH'] = ";".join([\
                g.app.root_path,
                os.path.abspath(os.path.join(_path, ".."))
            ])
            sp.append(subprocess.Popen(\
                ["minimo", "run", _name, "-s"],
                cwd = g.app.root_path,
                env = sp_env
            ))
        except:
            report_exception(_name, format_traceback())
            error(_("error.task.exception_in_case"), _name)

    for s in sp:
        s.wait()

# end
