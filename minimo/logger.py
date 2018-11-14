# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


import os
import sys
import time
import logging
from .globals import SECTION_SPLITTER
from .helpers import flatten


SUCCESS = logging.INFO + 1
logging.addLevelName(SUCCESS, "SUCCESS")
FAILURE = logging.ERROR + 1
logging.addLevelName(FAILURE, "FAILURE")
REPORT = logging.CRITICAL + 1
logging.addLevelName(REPORT, "REPORT")

_LVL_PREFIX = {
    logging.INFO: "",
    logging.ERROR: "[ERROR] ",
    logging.WARNING: "[WARNING] ",
    SUCCESS: "[SUCCESS] ",
    FAILURE: "[FAILURE] ",
    REPORT: ""
}


class MoFilter(logging.Filter):
    """MO filter to print line number (message count) into log message."""

    def filter(self, record):
        record.lvl = _LVL_PREFIX[record.levelno]
        return True


class Logger(object):
    """print log to log file and stdout.

    log directory will be placed under
    project.root/logs. by default, it will create two kinds of log file which
    are fulltrace and errors only.

    :param case: task case name, used as log file prefix.
    :param suite: task suite name, if specified suite name, mini-mo will create
                  suite folder to contain all case log files.
    :param root: project root, log file will be created under root/log.
    :param max_flush_count: threshold to flush message to log file,
                            set to 10 by default.

    usage::
        logger = Logger(
            "case name",
            "suite name",
            "path/to/project/root"
        ).open()

        logger.info("information")
        logger.warning("warning message")
        logger.error("error message")

        logger.summary()
        logger.close()
    """

    def __init__(
        self,
        case="my_case",
        suite=None,
        root=".",
        max_flush_count=10
    ):
        self.case = case
        self.suite = suite
        self.root = os.path.join(root, "log")
        self.logpath = ""
        self.counters = {
            "error": 0,
            "warning": 0,
            "success": 0,
            "failure": 0
        }

        self.__flush_count = 0
        self.__max_flush_count = max_flush_count

        # store file handlers as:
        # {
        #    level: [handlers]
        # }
        self.__filehandlers = {}

    def open(
        self,
        stdout=True,
        outputs={
            "fulltrace": logging.INFO,
            "error": logging.ERROR,
            "report": REPORT
        }
    ):
        """open log system and print log to the specified outputs"""

        # create logger
        self.__logger = logging.getLogger("log-{0}".format(self.case))
        self.__logger.setLevel(logging.INFO)

        # create stdout/file handler and set level
        self.__logger.addFilter(MoFilter())
        formatter = \
            logging.Formatter("[%(asctime)s] %(lvl)s%(message)s")
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")

        # add stdout handlers to logger
        if stdout:
            stdout = logging.StreamHandler(sys.stdout)
            stdout.setLevel(logging.NOTSET)
            stdout.setFormatter(formatter)
            self.__logger.addHandler(stdout)

        # add file handlers to logger
        if len(outputs) > 0:
            if self.suite is not None:
                self.logpath = os.path.join(self.root, self.suite)
            else:
                self.logpath = os.path.join(self.root, self.case)
            basename = os.path.join(self.logpath,
                                    "{0}_{1}".format(self.case, timestamp))

            # check out dirs
            if not os.path.exists(self.logpath):
                os.makedirs(self.logpath)

            for term, level in outputs.items():
                handler = logging.FileHandler(
                    "{0}.{1}.log".format(basename, term))
                handler.setLevel(level)
                handler.setFormatter(formatter)
                if level not in self.__filehandlers:
                    self.__filehandlers[level] = []
                self.__filehandlers[level].append(handler)
                self.__logger.addHandler(handler)

        # initialize flags
        self.__closed = False

        return self

    def close(self):
        """close log system, flush all messages to log file,
        and clear message counters
        """
        if not self.__closed:
            for k in self.counters.keys():
                self.counters[k] = 0

            try:
                self.__flush_count = 0
                for handler in flatten(self.__filehandlers.values()):
                    handler.flush()
                    self.__logger.removeHandler(handler)
                    handler.close()
            except Exception:
                # do nothing
                pass

            # reset flags
            self.__closed = True

    def summary(self, *args, **kwargs):
        """print summary as normal information"""
        self.info(
            "\n%s \
             \nSUCCESS: %d \
             \nFAILURE: %d \
             \nERROR: %d \
             \nWARNING: %d \
             \nDURATION: %s" % (
                SECTION_SPLITTER,
                self.counters["success"],
                self.counters["failure"],
                self.counters["error"],
                self.counters["warning"],
                kwargs["duration"]))

    def info(self, message):
        """print normal information"""
        self._write(message, logging.INFO)

    def error(self, message):
        """print error message"""
        self.counters["error"] += 1
        self._write(message, logging.ERROR)

    def warning(self, message):
        """print warning message"""
        self.counters["warning"] += 1
        self._write(message, logging.WARNING)

    def success(self, message):
        """print task success message"""
        self.counters["success"] += 1
        self._write(message, SUCCESS)

    def fail(self, message):
        """print task failure message"""
        self.counters["failure"] += 1
        self._write(message, FAILURE)

    def report(self, message):
        """print report information to report file"""

        # remove error handler
        errs = self.__filehandlers[logging.ERROR]
        for handler in errs:
            self.__logger.removeHandler(handler)

        self._write(message, REPORT)

        for handler in errs:
            self.__logger.addHandler(handler)

    def _write(self, message, level=logging.INFO):
        """print message to log handler according to logging level.

        message format looks like:
            '[timestamp] level-prefix message'
        """
        if not self.__closed:
            self.__logger.log(level, message)
            self.__flush_count += 1
            if self.__flush_count >= self.__max_flush_count:
                for handler in flatten(self.__filehandlers.values()):
                    handler.flush()
                self.__flush_count = 0

# end
