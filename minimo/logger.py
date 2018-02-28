# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


import os
import sys
import time
import logging
from .globals import g


SUCCESS = logging.INFO + 1
logging.addLevelName(SUCCESS, "SUCCESS")
FAILURE = logging.ERROR + 1
logging.addLevelName(FAILURE, "FAILURE")

_LVL_PREFIX = {
    logging.INFO: "",
    logging.ERROR: "[ERROR] ",
    logging.WARNING: "[WARNING] ",
    SUCCESS: "[SUCCESS] ",
    FAILURE: "[FAILURE] "
}
    
class Logger(object):
    """print log to log file and stdout. log directory will be 
    placed under project.root/logs. by default, it will create 
    two kinds of log file which are fulltrace and errors only."""
    
    def __init__(
        self, 
        case = "my_case", 
        suite = None, 
        root = ".", 
        max_flush_count = 10
    ):       
        self.case = case
        self.suite = suite
        self.root = os.path.join(root, "logs")
        self.counters = { "error": 0, "warning": 0, "success": 0, "failure": 0 }
        
        self.__flush_count = 0
        self.__max_flush_count = max_flush_count
        self.__filehandlers = []

    def open(
        self,
        stdout = True,
        outputs = {
            "fulltrace": logging.INFO,
            "error": logging.ERROR,
        }
    ):
        """open log system by the specified outputs"""

        # create logger
        self.__logger = logging.getLogger("log-{0}".format(self.case))
        self.__logger.setLevel(logging.INFO)

        # create stdout/file handler and set level
        formatter = logging.Formatter("[%(asctime)s] %(message)s") 
        timestamp = time.strftime("%Y_%m_%d_%H_%M_%S")

        # add stdout handlers to logger
        if stdout:
            stdout = logging.StreamHandler(sys.stdout)
            stdout.setLevel(logging.INFO)
            stdout.setFormatter(formatter)
            self.__logger.addHandler(stdout)

        # add file handlers to logger
        if len(outputs) > 0:
            if self.suite is not None:
                dirpath = os.path.join(self.root, self.suite)
            else:
                dirpath = os.path.join(self.root, self.case)
            basename = os.path.join(dirpath, \
                "{0}_{1}".format(self.case, timestamp))  
            
            # check out dirs
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)

            for term, level in outputs.items():
                handler = logging.FileHandler("{0}.{1}.log".format(basename, term))
                handler.setLevel(level)
                handler.setFormatter(formatter)
                self.__filehandlers.append(handler)
                self.__logger.addHandler(handler)
        
        self.__closed = False   
        return self
    
    def close(self):
        """close log system, flush all messages to log file, 
        and clear message counters"""
        if not self.__closed:
            self.counters = { "error": 0, "warning": 0, "success": 0, "failure": 0 }

            try:
                self.__flush_count = 0
                for handler in self.__filehandlers:
                    handler.flush()
                    self.__logger.removeHandler(handler)
                    handler.close()
            except:
                # do nothing
                pass
            self.__closed = True
            
    def info(self, message, *args, **kwargs):
        self._write(message.format(*args, **kwargs), logging.INFO)
        
    def error(self, message, *args, **kwargs):
        """print error message"""
        self.counters["error"] += 1
        self._write(message.format(*args, **kwargs), logging.ERROR)
        
    def warning(self, message, *args, **kwargs):
        """print warning message"""
        self.counters["warning"] += 1
        self._write(message.format(*args, **kwargs), logging.WARNING)
        
    def success(self, message, *args, **kwargs):
        """print task success message"""
        self.counters["success"] += 1
        self._write(message.format(*args, **kwargs), SUCCESS)
        
    def fail(self, message, *args, **kwargs):
        """print task failure message"""
        self.counters["failure"] += 1
        self._write(message.format(*args, **kwargs), FAILURE)
    
    def _write(self, message, level = logging.INFO):
        """print message to log handler according to logging level.

        message format looks like: 
            '[timestamp] #line-no level-prefix message' 
        """
        if not self.__closed:
            _printed = "#{0} {1}{2}".format(g.line, _LVL_PREFIX[level], message)
            try:        
                self.__logger.log(level, _printed)
                g.line += 1
                self.__flush_count += 1
                if self.__flush_count >= self.__max_flush_count:
                    for handler in self.__filehandlers:
                        handler.flush()
                    self.__flush_count = 0        
            except:
                print _printed
