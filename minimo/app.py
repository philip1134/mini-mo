# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#

import os
import re
import sys
import time
import runpy
import collections
import gettext  
from functools import wraps
from .globals import *
from .helpers import *
from .config import Config


_routes = {}
def bind(cmd):
    """bind command to callback."""
    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        _routes[cmd] = f
        return decorated_func
    return decorator

class MoApplication(object):
    """the MoApplication object implements the basic entry of minimo framework"""

    config = Config({
        "name": "minimo",
        "bin": "minimo",
        "root_path": ".",
        "locale": "zh_CN"
    })

    def __init__(self):
        self.__errors = []
        self.__task_suite = None
        gettext.translation("minimo", 
                            os.path.join(os.path.dirname(__file__), "locales"), 
                            languages = [self.config.locale]).install()
        g.app = self

    def project_name(self):
        return self.config.name

    def root_path(self):
        return self.config.root_path

    def bin_name(self):
        return self.config.bin

    def task_suite(self):
        return self.__task_suite

    def report_case_exception(self, case_name, reason):
        self.__errors.append(_("info.report_case_exception").format(case_name, reason))
        
    def run(self):
        """parse cli options"""
        
        try:
            i = sys.argv.index(self.bin_name())
            cmd = sys.argv[i+1]
            options = sys.argv[i+2:]
            _routes[cmd](self, options)
        except:
            self.print_wrong_usage()
            # print format_traceback()

    def parse_cli(self):
        parser = argparse.ArgumentParser(usage = _("help.app"))
        parser.add_argument("new")

    @bind("run")
    def run_cases(self, options):
        """run task cases"""
        tasks = collections.OrderedDict()
        
        sum = 0
        task_suite = "task"               
        
        # check case runner
        for case in set(options):
            runner_path = os.path.join(self.root_path(), "cases", case)
            task_suite = "{0}_{1}".format(task_suite, case.replace("/", "_"))
            
            # loop for __main__.py
            valid_case = False
            for _root, _dirs, _files in os.walk(runner_path):
                if "__main__.py" in _files:
                    _name = _root.replace(os.path.join(self.root_path(), "cases"), "")[1:]
                    valid_case = True
                    if not tasks.has_key(_name):
                        tasks[_name] = _root
                        info(_("info.add_task", _name))
                    
            if not valid_case:
                warning(_("warning.not_standard_case"), case, self.project_name())
                self.report_case_exception(case, _("info.not_standard_case"))
                
        self.__task_suite = "{0}_{1}".format(task_suite, \
                time.strftime("%Y_%m_%d_%H_%M_%S"))   
             
        for _name, _path in tasks.items():
            try:
                info(_("info.executing_task"), _name)
                _stacks = re.split(r"/|\\", _name)
                _proj_path = os.path.join(self.root_path(), "cases", _stacks[0])
                if len(_stacks) > 1 and _proj_path not in sys.path:
                    sys.path.insert(0, _proj_path)
                    
                runpy.run_path(_path)
            except:
                tb = format_traceback()
                self.report_case_exception(_name, tb)
                error(_("error.exception_in_case"), _name)
            sum += 1
             
        info(_("info.report_mission_complete"), BLOCK_SPLITTER, sum, len(self.__errors))  
        if len(self.__errors) > 0:
            info(u"异常任务包括:\nx {0}".format("\nx ".join(self.__errors)))
    
    @bind("help")
    def print_usage(self, *args):
        """show cli usage"""
        info(_("help.app"), project_name = self.project_name(), bin_name = self.bin_name())          

    def print_wrong_usage(self):
        error(_("error.wrong_usage"))
        self.print_usage()  
# end
