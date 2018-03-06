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

@register("help", "help.help", True)
def minimo_print_usage(*args):
    """show usage"""

    sub_commands = ""
    for cmd, conf in g.routes.items():
        if conf["trans"]:
            _help = _(conf["help"])
        else:
            _help = conf["help"]
        sub_commands += "\n* {0} - {1}\n".format(cmd, _help) 

    info(_("help.app"), 
        project_name = g.app.name, 
        sub_commands = sub_commands)   

@register("run", "help.run", True)
def minimo_run_cases(args = {}):
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
                _name = _root.replace(os.path.join(g.app.root_path, "cases"), "")[1:]
                valid_case = True
                if not tasks.has_key(_name):
                    tasks[_name] = _root
                    info(_("info.add_task"), _name)
                
        if not valid_case:
            warning(_("warning.not_standard_case"), case, g.app.name)
            report_exception(case, _("info.not_standard_case"))
            
    g.task_suite = "{0}_{1}".format(task_suite, time.strftime("%Y_%m_%d_%H_%M_%S"))   
         
    if "concorrence" == g.app.run_cases and not args.has_key("s"):
        _run_cases_concorrence(tasks)
    else:
        _run_cases_serial(tasks)
         
    info(_("info.report_mission_complete"), BLOCK_SPLITTER, len(tasks), len(g.errors))  
    if len(g.errors) > 0:
        info(_("info.failed_tasks"), "\nx ".join(g.errors))

def _run_cases_serial(tasks = {}):
    """serial type to run cases"""

    for _name, _path in tasks.items():
        try:
            info(_("info.executing_task"), _name)
            module_path = os.path.abspath(os.path.join(_path, ".."))
            if module_path not in sys.path:
                sys.path.insert(0, module_path)
                
            runpy.run_path(_path)
        except:
            report_exception(_name, format_traceback())
            error(_("error.exception_in_case"), _name)

def _run_cases_concorrence(tasks = {}):
    """concorrence type to run cases"""

    sp = []
    for _name, _path in tasks.items():
        try:
            info(_("info.executing_task"), _name)
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
            error(_("error.exception_in_case"), _name)     

    for s in sp:
        s.wait()   