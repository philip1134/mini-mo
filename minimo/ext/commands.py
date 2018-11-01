# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import os
import sys
import time
import click
import runpy
import fnmatch
import collections
from ..helpers import *
from ..globals import *
from minimo import __version__


@click.command("version")
def print_version():
    """print minimo version number."""
    info("minimo {}".format(__version__))


@click.command("ls")
@click.argument("patterns", nargs=-1)
def list_cases(patterns):
    """list all standard task cases.

    usage:
        $ minimo ls [pattern...]

    "pattern" supports Unix shell-style wildcards, such as * or ?.
    if not specified "pattern", it will list all standard cases' names under
    "cases" folder. if specified "pattern", it will search the case name by
    "pattern". can give multiple patterns, such as：
        $ minimo ls foo bar*
    """

    cases = []
    pattern = "|".join([fnmatch.translate(ptn) for ptn in patterns])

    # loop for standard case
    case_dir = os.path.join(g.app.root_path, "cases")
    for _root, _dirs, _files in os.walk(case_dir):
        if "__main__.py" in _files:
            _name = _get_case_name(_root)
            if pattern:
                if re.match(pattern, _name):
                    cases.append(_name)
            else:
                cases.append(_name)

    result = sorted(cases)
    info("\n".join(result))

    return result


@click.command("run")
@click.argument("cases", nargs=-1)
def run_cases(cases):
    """run task cases."""

    tasks = collections.OrderedDict()
    task_suite = "task"

    # check case runner
    for case in set(cases):
        runner_path = os.path.join(g.app.root_path, "cases", case)
        task_suite = "{0}_{1}".format(task_suite, case.replace("/", "_"))

        # loop for __main__.py
        valid_case = False
        for _root, _dirs, _files in os.walk(runner_path):
            if "__main__.py" in _files:
                _name = _get_case_name(_root)
                valid_case = True
                if _name not in tasks:
                    tasks[_name] = _root
                    info("add task %s" % _name)

        if not valid_case:
            warning(
                "%s is not %s standard case, please run it respectively." % (
                    case, g.app.name))
            report_exception(case, "not standard case")

    g.task_suite = "{0}_{1}".format(task_suite,
                                    time.strftime("%Y_%m_%d_%H_%M_%S"))

    if "concorrence" == g.app.run_cases and "s" not in args:
        _run_cases_concurrently(tasks)
    else:
        _run_cases_serially(tasks)

    stage('\n\n%s\nmission complete!\n'
          'totally %s cases were executed, %s cases raised exception.' %
          (BLOCK_SPLITTER, len(tasks), len(g.errors)))
    if len(g.errors) > 0:
        stage("failed tasks:\nx %s" % "\nx ".join(g.errors))


def _run_cases_serially(tasks):
    """serial type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for task
                  module, task should have __main__ entry.
    """

    for _name, _path in tasks.items():
        try:
            stage("run task %s" % _name)
            module_path = os.path.abspath(os.path.join(_path, ".."))
            if module_path not in sys.path:
                sys.path.insert(0, module_path)

            runpy.run_path(_path)
        except Exception:
            report_exception(_name, format_traceback())
            error("exception occured while performing '%s'" % _name)


def _run_cases_concurrently(tasks):
    """concorrence type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for task
                  module, task should have __main__ entry.
    """

    sp = []
    for _name, _path in tasks.items():
        try:
            stage("run task %s" % _name)
            sp_env = os.environ.copy()
            sp_env['PYTHONPATH'] = ";".join([
                g.app.root_path,
                os.path.abspath(os.path.join(_path, ".."))
            ])
            sp.append(subprocess.Popen(
                ["minimo", "run", _name, "-s"],
                cwd=g.app.root_path,
                env=sp_env
            ))
        except Exception:
            report_exception(_name, format_traceback())
            error("exception occured while performing '%s'" % _name)

    for s in sp:
        s.wait()


def _get_case_name(case_path):
    """extract case name from case path."""
    return case_path.replace(os.path.join(
        g.app.root_path, "cases"), "")[1:].replace("\\", "/")
