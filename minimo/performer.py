# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


import os
import copy
import yaml
from .globals import *
from .utils import *
from .logger import Logger


class Performer:
    """mini-mo base performer to perform task case.

    :attr name: performer name
    :attr app: ref of application instance
    :attr config: deepcopy of project config from config.yml
    """

    def __init__(
        self,
        name,
        logger=None,
        case_path=None
    ):
        """performer constructor

        :param name: task name
        :param logger:
            logging handler, if set to none, will use minimo style logger.

            for customized logger, it should respond to the following methods:
                * open(): setup logger staff
                * close(): teardown logger
                * info(message, *args, **kwargs): print normal information
                                                  message
                * warning(message, *args, **kwargs): print warning message
                * error(message, *args, **kwargs): print error message
                * success(message, *args, **kwargs): print task success message
                * fail(message, *args, **kwargs): print task failure message
        :param case_path: case folder path
        """

        super(Performer, self).__init__()

        self.name = name
        self.app = ctx.app

        if case_path is None:
            self.case_path = None
        else:
            self.case_path = os.path.dirname(case_path)

        self._load_config()

        # setup logger
        if logger is None:
            self.logger = Logger(name=self.name,
                                 output_path=ctx.output_path,
                                 stdout=ctx.app.echo_to_stdout)
        else:
            self.logger = logger

    def run(self):
        """execute performer"""

        self._setup()

        self._do_before_actions() and \
            self._do_action_steps() and \
            self._do_after_actions()

        self._teardown()

# protected
    def _setup(self):
        """setup environment before performer actions"""

        # start timer
        ctx.counter.start_timer_for(self.name)

    def _teardown(self):
        """tear down environment after performer actions"""

        # stop timer
        ctx.counter.stop_timer_for(self.name)

    def _load_config(self):
        """load case configuration under case-folder/config.yml"""

        # copy global config
        self.config = copy.deepcopy(ctx.config)

        # copy case config
        if self.case_path is not None:
            config_path = os.path.join(self.case_path, "config.yml")
            if os.path.exists(config_path):
                with open(config_path, mode="r", encoding="utf-8") as f:
                    # load yml to config
                    cfg = yaml.full_load(f.read())
                    if isinstance(cfg, dict):
                        self.config.update(cfg)

    def _do_before_actions(self):
        """execute before_action functions"""
        return self._do_actions(
            ctx.callbacks.get_before_actions(self._get_caller_id()))

    def _do_action_steps(self):
        """execute action_step functions"""
        return self._do_actions(
            ctx.callbacks.get_action_steps(self._get_caller_id()), True)

    def _do_after_actions(self):
        """execute after_step functions"""
        return self._do_actions(
            ctx.callbacks.get_after_actions(self._get_caller_id()))

    def _do_actions(self, action_list, action_step=False):
        result = True
        for func in action_list:
            self.logger.info("[%s] start action '%s'..." % (
                self.name, func.__name__))

            try:
                r = func(self)
            except Exception:
                r = False
                tb = format_traceback()
                ctx.counter.append_exception(self.name, tb)
                self.logger.error(
                    '[%s] error occured, please check out your task code!'
                    '\n%s' % (self.name, tb))

            if isinstance(r, bool):
                _r = r
            else:
                _r = True

            if action_step:
                if _r:
                    self.logger.success("[%s] succeed to perform '%s'" % (
                                        self.name,
                                        func.__name__))
                else:
                    self.logger.fail("[%s] fail to perform '%s'" % (
                                     self.name,
                                     func.__name__))
            elif not _r:
                result = False
                self.logger.fail("[%s] error occured while performing '%s'" % (
                                 self.name,
                                 func.__name__))
                break

        return result

    def _get_caller_id(self):
        return "%s.%s" % (self.__module__, self.__class__.__name__)

# end
