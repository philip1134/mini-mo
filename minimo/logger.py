# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


import os
import sys
import logging
from .globals import ctx


SUCCESS = logging.INFO + 1
logging.addLevelName(SUCCESS, "SUCCESS")
FAILURE = logging.ERROR + 1
logging.addLevelName(FAILURE, "FAILURE")

_LVL_PREFIX = {
    logging.INFO: "INFO",
    logging.ERROR: "ERROR",
    logging.WARNING: "WARNING",
    SUCCESS: "SUCCESS",
    FAILURE: "FAILURE",
}


class MoFilter(logging.Filter):
    """MO filter to map customized level."""

    def filter(self, record):
        record.lvl = _LVL_PREFIX[record.levelno]
        return True


class Logger:
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
            name="case name",
            output_path="path/to/project/output_path"
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
        stdout=True,
        outputs={
            "fulltrace": logging.INFO,
            "error": logging.ERROR,
        },
        log_format="%(asctime)s %(process)d:%(thread)d %(lvl)s %(message)s"
    ):
        super(Logger, self).__init__()

        self.name = name
        self.output_path = output_path
        self.stdout = stdout
        self.outputs = outputs
        self.max_flush_count = max_flush_count

        self._closed = True
        self._flush_count = 0
        self._format = log_format

        # store file handler as:
        # {
        #    name: handler
        # }
        self._handlers = {}

        # setup logger
        self.open()

    def __del__(self):
        """destructor"""

        self.close()

    def open(self):
        """open log system and print log to the specified outputs"""

        if self._closed:
            # create logger
            self._logger = logging.getLogger("log-{0}".format(self.name))
            self._logger.setLevel(logging.INFO)

            # create stdout/file handler and set level
            self._logger.addFilter(MoFilter())
            formatter = \
                logging.Formatter(self._format)

            # add stdout handlers to logger
            if self.stdout:
                stdout = logging.StreamHandler(sys.stdout)
                stdout.setLevel(logging.NOTSET)
                stdout.setFormatter(formatter)
                self._logger.addHandler(stdout)
                self._handlers["stdout"] = stdout

            # add file handlers to logger
            if len(self.outputs) > 0:
                basename = os.path.join(self.output_path, self.name)

                # check out dirs
                if not os.path.exists(self.output_path):
                    try:
                        # may conflict in concorrence running type
                        os.makedirs(self.output_path)
                    except Exception:
                        pass

                for name, level in self.outputs.items():
                    handler = logging.FileHandler(
                        "{0}.{1}.log".format(basename, name),
                        encoding="utf-8")
                    handler.setLevel(level)
                    handler.setFormatter(formatter)
                    self._handlers[name] = handler
                    self._logger.addHandler(handler)

            self._closed = False
        return self

    def close(self):
        """manually close log system, flush all messages to log file,
        and clear message counters.

        when the logging module is imported, it registers logging.shutdown()
        as an exit handler, that will perform an orderly shutdown by flushing
        and closing all handlers. here we provide this function to release
        resources manually if necessary in the whole working flow.
        """

        if not self._closed:
            try:
                self._flush_count = 0
                for handler in self._handlers.values():
                    # handler calls flush() in close()
                    handler.close()
                    self._logger.removeHandler(handler)
            except Exception:
                # do nothing
                pass

            # reset flags
            self._closed = True

    def info(self, message):
        """print normal information"""

        self.write(message, logging.INFO)

    def error(self, message):
        """print error message"""

        ctx.counter.append_error(self.name, message)
        self.write(message, logging.ERROR)

    def warning(self, message):
        """print warning message"""

        ctx.counter.append_warning(self.name, message)
        self.write(message, logging.WARNING)

    def success(self, message):
        """print task success message"""

        ctx.counter.append_success(self.name, message)
        self.write(message, SUCCESS)

    def fail(self, message):
        """print task failure message"""

        ctx.counter.append_failure(self.name, message)
        self.write(message, FAILURE)

    def write(self, message, level=logging.INFO):
        """print message to log handler according to logging level.

        message format looks like:
            '[timestamp] level-prefix message'
        """

        if not self._closed:
            self._logger.log(level, message)
            self._flush_count += 1
            if self._flush_count >= self.max_flush_count:
                self.flush()

    def flush(self):
        """flush messages to handlers"""

        for handler in self._handlers.values():
            handler.flush()
        self._flush_count = 0

    def get_filehandler(self, name):
        """get file handler by the specified name, if there's no such name,
        returns None.
        """

        return self._handlers.get(name)


class StdoutToFileLogger(Logger):
    """redirect stdout to log file"""

    def __init__(
        self,
        name="my_case",
        output_path=".",
        outputs={
            "fulltrace": logging.INFO
        }
    ):
        super(StdoutToFileLogger, self).__init__(
            name=name,
            stdout=False,
            output_path=output_path,
            outputs=outputs
        )

    def write(self, message, level=logging.INFO):
        """override write function to handle byte type message"""

        if message is None:
            _msg = ""
        else:
            _msg = message.decode("utf-8")
        self._logger.log(level, _msg)

# end
