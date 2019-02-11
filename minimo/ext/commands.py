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
import threading
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
    case_dir = os.path.join(ctx.app.root_path, "cases")
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
def run_suite(cases):
    """run task suite."""

    tasks = collections.OrderedDict()
    task_suite = "task"

    # check case runner
    for case in set(cases):
        runner_path = os.path.join(ctx.app.root_path, "cases", case)
        task_suite = "{0}_{1}".format(task_suite, case.replace("/", "_"))

        # loop for __main__.py
        valid_case = False
        for _root, _dirs, _files in os.walk(runner_path):
            if "__main__.py" in _files:
                _name = _get_case_name(_root)
                valid_case = True
                if _name not in tasks:
                    tasks[_name] = _root
                    info("add task '%s'" % _name)

        if not valid_case:
            warning(
                "%s is not %s standard case, please run it respectively." % (
                    case, ctx.app.name))
            ctx.counter.append_exception(case, "not standard case")

    # append timestamp
    ctx.suite_name = "{0}_{1}".format(task_suite,
                                      time.strftime("%Y_%m_%d_%H_%M_%S"))

    ctx.output_path = os.path.join(ctx.app.root_path, "log", ctx.suite_name)

    if "concorrence" == ctx.app.running_type:
        _run_suite_concurrently(tasks)
    else:
        _run_suite_serially(tasks)

    ctx.reporter.report()


def run_case(case, path, context):
    """run case from the specified path as named 'case'."""

    try:
        stage("running task '%s'..." % case)

        module_path = os.path.abspath(os.path.join(path, ".."))
        if module_path not in sys.path:
            sys.path.insert(0, module_path)

        runpy.run_path(path)
    except Exception:
        tb = format_traceback()
        context.counter.append_exception(case, tb)
        error("exception occured while performing '%s':\n%s" % (case, tb))


def _run_suite_serially(tasks):
    """serial type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for task
                  module, task should have __main__ entry.
    """

    for _name, _path in tasks.items():
        run_case(_name, _path, ctx)


def _run_suite_concurrently(tasks):
    """concorrence type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for
                  task module, task should have __main__ entry.
    """

    threads = []
    for _name, _path in tasks.items():
        threads.append(threading.Thread(
            name=_name,
            target=run_case,
            kwargs={
                "case": _name,
                "path": _path,
                "context": ctx
            })
        )

    for t in threads:
        t.join()


# def _run_suite_concurrently(tasks):
#     """concorrence type to run cases.

#     :param tasks: dict for tasks, key is task name, value is the path for
#                   task module, task should have __main__ entry.
#     """

#     sp = []
#     for _name, _path in tasks.items():
#         try:
#             sp_env = os.environ.copy()
#             sp_env['PYTHONPATH'] = ";".join([
#                 ctx.app.root_path,
#                 os.path.abspath(os.path.join(_path, ".."))
#             ])
#             sp.append(subprocess.Popen(
#                 ["minimo", "run", _name, "-s"],
#                 cwd=ctx.app.root_path,
#                 env=sp_env
#             ))
#         except Exception:
#             ctx.app.report_exception(_name, format_traceback())
#             error("exception occured while performing '%s'" % _name)

#     for s in sp:
#         s.wait()


def _get_case_name(case_path):
    """extract case name from case path."""

    return case_path.replace(os.path.join(
        ctx.app.root_path, "cases"), "")[1:].replace("\\", "/")
