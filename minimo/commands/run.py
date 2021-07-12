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
import collections
from ..utils import *
from ..globals import *
from .common import get_case_name, verify_root_path
from multiprocessing.dummy import Pool as ThreadPool


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
                        cases=["suite1", "suite2/case1", "suite2/case2"])
    """

    return run_suite_with_context(cases)


def run_suite_with_context(cases):
    """run suite main method"""

    if not verify_root_path(ctx):
        return None

    tasks = collections.OrderedDict()
    task_suite = "task"

    # check out data type
    if isinstance(cases, str):
        cases = [cases]

    # check case runner
    for case in set(cases):
        runner_path = os.path.join(ctx.app.inst_path, "cases", case)
        task_suite = "{0}_{1}".format(task_suite, case.replace("/", "_"))

        # loop for __main__.py
        valid_case = False
        for _root, _dirs, _files in os.walk(runner_path):
            if "__main__.py" in _files:
                _name = get_case_name(_root, ctx.app.inst_path)
                valid_case = True
                if _name not in tasks:
                    tasks[_name] = _root
                    info("add task '%s' with case path '%s'" % (_name, _root))

        if not valid_case:
            warning(
                "%s is not %s standard case, please run it respectively." % (
                    case, ctx.app.name))
            ctx.counter.append_exception(case, "not standard case")

    # append timestamp
    ctx.suite_name = "{0}_{1}".format(
        task_suite,
        time.strftime("%Y_%m_%d_%H_%M_%S")
    )
    ctx.output_path = os.path.join(
        ctx.app.inst_path, "log", ctx.suite_name)

    if "concorrence" == ctx.config.running_type:
        # check out max_thread_count
        if hasattr(ctx.config, "max_thread_count"):
            # up2date minimo version
            max_thread_count = ctx.config.max_thread_count
        elif hasattr(ctx.config, "max_process_count"):
            # previous minimo version
            max_thread_count = ctx.config.max_process_count
        else:
            # no such config, set to 10 threads by default
            max_thread_count = 10

        _run_suite_concurrently(tasks, ctx, max_thread_count)
    else:
        _run_suite_serially(tasks, ctx)

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


def _run_suite_serially(tasks, context):
    """serial type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for task
                  module, task should have __main__ entry.
    """

    for _name, _path in tasks.items():
        _run_case(_name, _path, context)


def _run_suite_concurrently(tasks, context, max_thread_count=10):
    """concorrence type to run cases.

    :param tasks: dict for tasks, key is task name, value is the path for
                  task module, task should have __main__ entry.

    :param max_thread_count: max thread count to run tasks.
    """

    if not isinstance(max_thread_count, int):
        error("max thread count is not number, please check out your config.")
        return

    if max_thread_count <= 0 or max_thread_count > 1000:
        max_thread_count = 1000

    info("prepare to run suite in %d thread." % max_thread_count)
    pool = ThreadPool(max_thread_count)

    for _name, _path in tasks.items():
        pool.apply_async(
            _run_case,
            kwds={
                "case": _name,
                "path": _path,
                "context": context
            })
    pool.close()
    pool.join()


# end
