# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


import os
import sys
import logging
from .globals import SECTION_SPLITTER, ctx
from .helpers import flatten


SUCCESS = logging.INFO + 1
logging.addLevelName(SUCCESS, "SUCCESS")
FAILURE = logging.ERROR + 1
logging.addLevelName(FAILURE, "FAILURE")

_LVL_PREFIX = {
    logging.INFO: "",
    logging.ERROR: "[ERROR] ",
    logging.WARNING: "[WARNING] ",
    SUCCESS: "[SUCCESS] ",
    FAILURE: "[FAILURE] ",
}


class MoFilter(logging.Filter):
    """MO filter to map customized level."""

    def filter(self, record):
        record.lvl = _LVL_PREFIX[record.levelno]
        return True


class Logger(object):
    """print log to log file and stdout.

    log directory will be placed under
    project.root/logs. by default, it will create two kinds of log file which
    are fulltrace and errors only.

    :param case: task case name, used as log file prefix.
    :param output_path: project output path, log file and report file will be
                        created under this path, normally it's `app_root/log`.
    :param max_flush_count: threshold to flush message to log file,
                            set to 10 by default.

    usage::
        logger = Logger(
            "case name",
            "path/to/project/output_path"
        )

        logger.info("information")
        logger.warning("warning message")
        logger.error("error message")

        logger.close()
    """

    def __init__(
        self,
        name="my_case",
        output_path=".",
        max_flush_count=10,
        setup=True,
        stdout=True
    ):
        self.name = name
        self.output_path = output_path

        self.__flush_count = 0
        self.__max_flush_count = max_flush_count

        # store file handlers as:
        # {
        #    level: [handlers]
        # }
        self.__filehandlers = {}

        if setup:
            self.open(stdout=stdout)

    def open(
        self,
        stdout=True,
        outputs={
            "fulltrace": logging.INFO,
            "error": logging.ERROR,
        }
    ):
        """open log system and print log to the specified outputs"""

        # create logger
        self.__logger = logging.getLogger("log-{0}".format(self.name))
        self.__logger.setLevel(logging.INFO)

        # create stdout/file handler and set level
        self.__logger.addFilter(MoFilter())
        formatter = \
            logging.Formatter("[%(asctime)s] %(lvl)s%(message)s")

        # add stdout handlers to logger
        if stdout:
            stdout = logging.StreamHandler(sys.stdout)
            stdout.setLevel(logging.NOTSET)
            stdout.setFormatter(formatter)
            self.__logger.addHandler(stdout)

        # add file handlers to logger
        if len(outputs) > 0:
            basename = os.path.join(self.output_path, self.name)

            # check out dirs
            if not os.path.exists(self.output_path):
                try:
                    # may conflict in concorrence running type
                    os.makedirs(self.output_path)
                except Exception:
                    pass

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

    def info(self, message):
        """print normal information"""

        self._write(message, logging.INFO)

    def error(self, message):
        """print error message"""

        ctx.counter.append_error(self.name, message)
        self._write(message, logging.ERROR)

    def warning(self, message):
        """print warning message"""

        ctx.counter.append_warning(self.name, message)
        self._write(message, logging.WARNING)

    def success(self, message):
        """print task success message"""

        ctx.counter.append_success(self.name, message)
        self._write(message, SUCCESS)

    def fail(self, message):
        """print task failure message"""

        ctx.counter.append_failure(self.name, message)
        self._write(message, FAILURE)

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
