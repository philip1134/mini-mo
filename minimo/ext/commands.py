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
from multiprocessing.dummy import Pool as ThreadPool
from minimo import __version__


@click.command("version")
def print_version():
    """print minimo version number.

    usage in cli mode:

        $ mmo version

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api",
                    root_path=instance_project_path)

        # version string
        version = mmo.call("version")
    """

    version = "minimo {}".format(__version__)

    info(version)
    return version


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

    if ctx.app.inst_path is None:
        error('not in minimo project root folder.')
        return []

    cases = []
    pattern = "|".join([fnmatch.translate(ptn) for ptn in patterns])

    # loop for standard case
    case_dir = os.path.join(ctx.app.inst_path, "cases")
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
    """run task suite.

    usage in cli mode:

        $ mmo run [case...]

    can specify some cases separated by whitespace as:

        $ mmo run case1 case2 case3

    and also can specify some suites (case group under one folder) as:

        $ mmo run suite1 suite2 suite3

    minimo will run all cases under those suites.

    tip: can use 'mmo' or 'minimo' as the main command after v0.4.0.

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api",
                    root_path=instance_project_path)

        # return output file path or None if all failed
        sorted_cases = mmo.call(
                        "run",
                        cases=["suite1", "suite2/case1", suite2/case2])
    """

    if ctx.app.inst_path is None:
        error('not in minimo project root folder.')
        return None

    tasks = collections.OrderedDict()
    task_suite = "task"

    # check case runner
    for case in set(cases):
        runner_path = os.path.join(ctx.app.inst_path, "cases", case)
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

    ctx.output_path = os.path.join(ctx.app.inst_path, "log", ctx.suite_name)

    if "concorrence" == ctx.app.running_type:
        _run_suite_concurrently(tasks)
    else:
        _run_suite_serially(tasks)

    return ctx.reporter.report()


def _run_case(case, path, context):
    """run case from the specified path as named 'case'."""

    try:
        stage("running task '%s'..." % case)

        module_path = os.path.abspath(os.path.join(path, ".."))
        if module_path not in sys.path:
            sys.path.insert(0, module_path)

        mainpy_path = os.path.join(path, "__main__.py")
        if os.path.basename(path) != "__main__.py" and \
           os.path.exists(mainpy_path):
            # definitely set the __main__.py path to
            # avoid multiple thread conflict
            _path = mainpy_path
        else:
            _path = path

        runpy.run_path(_path)

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
        _run_case(_name, _path, ctx)


def _run_suite_concurrently(tasks, max_process_count=50):
    """concorrence type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for
                  task module, task should have __main__ entry.

    :param max_process_count: max process count to run tasks.
    """

    if not isinstance(max_process_count, int):
        error("max process count is not number, please check out your config.")
        return

    if max_process_count <= 0 or max_process_count > 1000:
        max_process_count = 1000

    pool = ThreadPool(max_process_count)

    for _name, _path in tasks.items():
        pool.apply_async(
            _run_case,
            kwds={
                "case": _name,
                "path": _path,
                "context": ctx
            })
    pool.close()
    pool.join()


def _get_case_name(case_path):
    """extract case name from case path."""

    return case_path.replace(os.path.join(
        ctx.app.inst_path, "cases"), "")[1:].replace("\\", "/")

# end
