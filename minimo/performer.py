# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


from .globals import *
from .helpers import *
from .logger import Logger


class Performer(object):
    """mini-mo base performer to perform task case.

    :param name: task name
    :param logger:
        logging handler, if set to none, will use minimo style logger.

        for customized logger, it should respond to the following methods:
            * open(): setup logger staff
            * close(): teardown logger
            * info(message, *args, **kwargs): print normal information message
            * warning(message, *args, **kwargs): print warning message
            * error(message, *args, **kwargs): print error message
            * success(message, *args, **kwargs): print task success message
            * fail(message, *args, **kwargs): print task failure message
    """

    def __init__(
        self,
        name,
        logger=None
    ):
        super(Performer, self).__init__()

        self.name = name or __name__
        if logger is None:
            self.logger = Logger(name=self.name,
                                 output_path=ctx.output_path,
                                 stdout=ctx.app.is_cli_mode())
        else:
            self.logger = logger

    def run(self):
        """execute performer"""

        ctx.counter.start_timer_for(self.name)

        self.__do_before_actions() and \
            self.__do_action_steps() and \
            self.__do_after_actions()

        ctx.counter.stop_timer_for(self.name)
        self.logger.close()

    def __do_before_actions(self):
        """execute before_action functions"""
        return self.__do_actions(
            ctx.callbacks.get_before_actions(self.__get_caller_id()))

    def __do_action_steps(self):
        """execute action_step functions"""
        return self.__do_actions(
            ctx.callbacks.get_action_steps(self.__get_caller_id()), True)

    def __do_after_actions(self):
        """execute after_step functions"""
        return self.__do_actions(
            ctx.callbacks.get_after_actions(self.__get_caller_id()))

    def __do_actions(self, action_list, action_step=False):
        result = True
        for func in action_list:
            self.logger.info("start action %s..." % func.__desc__)

            try:
                r = func(self)
            except Exception:
                r = False
                tb = format_traceback()
                ctx.counter.append_exception(self.name, tb)
                self.logger.error(
                    'error occured, please check out your task code!'
                    '\n%s' % tb)

            if isinstance(r, bool):
                _r = r
            else:
                _r = True

            if action_step:
                if _r:
                    self.logger.success("succeed to perform %s/%s" % (
                                        self.name,
                                        func.__desc__ or func.__name__))
                else:
                    self.logger.fail("fail to perform %s/%s" % (
                                     self.name,
                                     func.__desc__ or func.__name__))
            elif not _r:
                result = False
                self.logger.fail("error occured while performing %s/%s" % (
                                 self.name,
                                 func.__desc__ or func.__name__))
                break

        return result

    def __get_caller_id(self):
        return "%s.%s" % (self.__module__, self.__class__.__name__)

# end
