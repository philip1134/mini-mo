# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#

import types
from .globals import *
from .logger import Logger
from .timer import Timer
from .helpers import *
        
class MoPerformer(object):
    """mini-mo base performer to perform task case."""
    
    def __init__(
        self, 
        name
    ):
        self.name = name
        self.logger = Logger(name, 
                        g.app.task_suite(),  
                        g.app.root_path()).open()
        self.__traceback = []

    def run(self):
        """execute performer"""

        self._setup()

        self.__do_before_actions() and \
        self.__do_action_steps() and \
        self.__do_after_actions()

        self._teardown()
    
    def _setup(self):
        """setup performer environment, in base class 
        we start timer to calculate the task duration"""

        self.__timer = Timer(__name__ + "_mo_performer")

    def _teardown(self):
        """tear down performer environment, in base class
        basically report task result and close log system."""

        self._report()
        self.logger.close()  

    def _report(self):
        """print mission report"""
        
        self.logger.info(_("info.performer_report"), 
            split = SECTION_SPLITTER, 
            success = self.logger.counters["success"],
            failure = self.logger.counters["failure"],
            error = self.logger.counters["error"],
            warning = self.logger.counters["warning"],
            exception = len(self.__traceback),
            duration = format_duration(self.__timer.duration()))       

        for tb in self.__traceback:
            self.logger.info(tb)

    def __report_exception_to_app(self, tb):
        if g.app is not None:
            g.app.report_case_exception(self.name, tb)

    def __do_before_actions(self):
        """execute before_action functions"""
        return self.__do_actions(g.callbacks.get_before_actions(self.__get_caller_id()))
    
    def __do_action_steps(self):
        """execute action_step functions"""
        return self.__do_actions(g.callbacks.get_action_steps(self.__get_caller_id()), True)
    
    def __do_after_actions(self):
        """execute after_step functions"""
        return self.__do_actions(g.callbacks.get_after_actions(self.__get_caller_id()))
         
    def __do_actions(self, action_list, action_step = False):
        result = True
        for func in action_list:
            self.logger.info(u"执行操作 {0}...".format(func.__desc__))
            
            try:
                r = func(self)
            except Exception, e:
                r = False
                tb = format_traceback()
                self.__traceback.append(u"异常操作: {0}\n{1}".format(func.__desc__, tb))
                self.__report_exception_to_app(tb)
                self.logger.error(u"执行时产生异常，请检查任务代码！\n{0}".format(tb))
                
            if type(r) is types.BooleanType:
                _r = r
            else:
                _r = True
                
            if action_step:
                if _r:
                    self.logger.success(u"成功执行 {0}/{1} ！".format(self.name, func.__desc__ or func.__name__))
                else:
                    self.logger.fail(u"在执行 {0}/{1} 时出现错误！".format(self.name, func.__desc__ or func.__name__))
            elif not _r:
                result = False
                self.logger.fail(u"在执行 {0}/{1} 时出现错误，操作中断！".format(self.name, func.__desc__ or func.__name__))
                break
            
        return result
    
    def __get_caller_id(self):
        return "{0}.{1}".format(self.__module__, self.__class__.__name__)
# end