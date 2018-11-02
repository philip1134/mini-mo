# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


from .globals import *
from .helpers import *
from .logger import Logger
from .timer import Timer


class Performer(object):
    """mini-mo base performer to perform task case.

    :param name: task name
    :param logger:
        logging handler, if set to none, will use minimo
        style logger. for customized logger, it should respond
        to the following methods:
            * open(): setup logger staff
            * close(): teardown logger
            * report(): print summary
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

        self.name = __name__
        if logger is None:
            self.logger = Logger(name,
                                 g.task_suite,
                                 g.app.root_path).open()
        else:
            self.logger = logger.open()

        self.__exceptions = []

    def run(self):
        """execute performer"""
        self.__timer = Timer(__name__ + "_mo_performer")

        self.__do_before_actions() and \
            self.__do_action_steps() and \
            self.__do_after_actions()

        self._report()
        self.logger.close()

    def _report(self):
        """print mission report"""
        self.logger.summary(
            duration=format_duration(self.__timer.duration()))

        for tb in self.__exceptions:
            self.logger.info(tb)

    def __do_before_actions(self):
        """execute before_action functions"""
        return self.__do_actions(
            g.callbacks.get_before_actions(self.__get_caller_id()))

    def __do_action_steps(self):
        """execute action_step functions"""
        return self.__do_actions(
            g.callbacks.get_action_steps(self.__get_caller_id()), True)

    def __do_after_actions(self):
        """execute after_step functions"""
        return self.__do_actions(
            g.callbacks.get_after_actions(self.__get_caller_id()))

    def __do_actions(self, action_list, action_step=False):
        result = True
        for func in action_list:
            self.logger.info("start action %s..." % func.__desc__)

            try:
                r = func(self)
            except Exception:
                r = False
                tb = format_traceback()
                self.__exceptions.append(
                    "failed action: %s\n%s" % (func.__desc__, tb))
                report_exception(self.name, tb)
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
