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
import inspect
import collections
import gettext  
from functools import wraps
from .globals import *
from .helpers import *


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

    def __init__(
        self, 
        project_name, 
        project_root, 
        project_bin = "minimo",
        locale = "zh_CN"
    ):
        caller = inspect.currentframe().f_back.f_locals["__file__"]

        self.__name = project_name
        self.__root = project_root or \
            os.path.abspath(os.path.join(os.path.dirname(caller), ".."))
        self.__bin = project_bin or \
            os.path.basename(caller)

        self.__errors = []
        
        gettext.translation("minimo", 
                            os.path.join(os.path.dirname(__file__), "locales"), 
                            languages = [locale]).install()
        g.app = self

    def project_name(self):
        return self.__name

    def root_path(self):
        return self.__root

    def bin_name(self):
        return self.__bin

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
        __task__ = "task"               
        
        # check case runner
        for case in set(options):
            runner_path = os.path.join(self.root_path(), "cases", case)
            __task__ = "{0}_{1}".format(__task__, case.replace("/", "_"))
            
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
                
        __task__ = "{0}_{1}".format(__task__, time.strftime("%Y_%m_%d_%H_%M_%S"))   
             
        for _name, _path in tasks.items():
            try:
                info(_("info.executing_task"), _name)
                _stacks = re.split(r"/|\\", _name)
                _proj_path = os.path.join(self.root_path(), "cases", _stacks[0])
                if len(_stacks) > 1 and _proj_path not in sys.path:
                    sys.path.insert(0, _proj_path)
                    
                runpy.run_path(_path, {"__task__": __task__})
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

    @bind("new")
    def create_cases(self, options):
        """create task case from template"""
        # author name is required
        try:
            index_author_flag = options.index("-a")
            options.pop(index_author_flag)
            author = options.pop(index_author_flag)
        except ValueError:
            error(_("error.case_author_name_required"), self.bin_name())
            return

        info(_("info.prepare_to_create_case"))
        for case in set(options):
            # checking templates
            dirs = ["cases"] + case.split("/")
            template_dir = None
            while len(dirs) > 0:
                dirs.pop()
                _templatedir_lang = os.path.join(self.root_path(), *(dirs + ["templates", "python"]))
                _templatedir = os.path.join(self.root_path(), *(dirs + ["templates"]))
                if os.path.exists(_templatedir_lang):
                    template_dir = _templatedir_lang
                    break
                elif os.path.exists(_templatedir):
                    template_dir = _templatedir
                    break                    
                
            if template_dir is None:
                warning(_("warning.abort_creating_case_for_no_template"), case)
            else:
                # checking target path
                target = os.path.join(self.__root, "cases", case)
                if os.path.exists(target):
                    warning(_("warning.abort_creating_case_for_existence"), case)
                    continue
                else:
                    info(_("info.creating_case_dir"), case)
                    os.makedirs(target)

                info(_("info.creating_case_by_template"), \
                    template_dir.replace(self.root_path(), "%s.root"%self.project_name()))
                
                # copy files
                for dirpath, dirs, files in os.walk(template_dir):
                    for file in files:
                        self._copy_template_file(
                            os.path.join(target, file.replace(".template", "")), 
                            os.path.join(dirpath, file), 
                            os.path.basename(case), author)
                
                info(_("info.case_created"), self.project_name())

    def print_wrong_usage(self):
        error(_("error.wrong_usage"))
        self.print_usage()  

    @staticmethod
    def _copy_template_file(dest, src, case_name, author):
        try: 
            with open(src, "r") as src_file:
                content = src_file.read()
               
            content = re.sub(r"\{\s*\{\s*name\s*\}\s*\}", case_name, content) 
            content = re.sub(r"\{\s*\{\s*author\s*\}\s*\}", author, content) 
            content = re.sub(r"\{\s*\{\s*date\s*\}\s*\}", time.strftime("%Y-%m-%d"), content) 
            f = open(dest, "w")
            f.write(content)
            f.close()

            info(u"创建 {0}".format(os.path.basename(dest)))
        except:
            warning(u"创建文件 {0} 失败，请重新创建这个文件！\n失败原因:\n{1}".format(\
                os.path.basename(dest)), format_traceback())
# end
