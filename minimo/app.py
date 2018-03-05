# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import gettext 
import importlib
from .globals import *
from .helpers import *


class MoApplication(object):
    """the MoApplication object implements the basic entry of minimo framework"""

    # project name, set in project instance
    name = "minimo"

    # project root path, auto set in project instance
    root_path = None

    # project interface, currently supported "cli", "api", default is "cli"
    #   cli: call commands/functions as command line interface
    #   api: call commands/functions as api
    interface = "cli"

    # case running type, should be "serial" or "concorrence", default is "serial"
    #   serial: run cases one by one
    #   concorrence: run cases concorrently by subprocess.
    run_cases = "serial"

    # project locale, currently supports zh_CN, en_US. default is zh_CN
    locale = "zh_CN"

    # project modules path, which will be inserted into sys.path at application 
    # started. by default, "lib", "ext", "cases", "vendors" will be added mandatory.
    modules_path = []
    mandatory_modules_path = ["lib", "ext", "cases", "vendors"]

    def __init__(self):
        gettext.translation("minimo", 
                            os.path.join(os.path.dirname(__file__), "locales"), 
                            languages = [self.locale]).install()
        g.app = self

    def run(self, options = {}):
        """application runner"""
        
        try:
            if "cli" == self.interface:
                _options = self.parse_cli()
            else:
                _options = options
        
            cmd = _options.pop("cmd")
            self.add_extensions()
            if g.routes.has_key(cmd):
                self.add_modules_path()
                getattr(self.__ext, g.routes[cmd]["handler"])(_options)
            else:
                error(_("error.unrecognized_command"))
        except:
            error(_("error.wrong_usage"))
            # print format_traceback()

    def add_modules_path(self):
        """walk through modules_path, if there's __init__.py, the folder will 
        be added into sys.path"""

        if self.root_path is None:
            return

        for target in set(self.modules_path + self.mandatory_modules_path):
            target_dir = os.path.join(self.root_path, target)
            if os.path.exists(target_dir):
                for dirpath, dirs, files in os.walk(target_dir):
                    if "__init__.py" in files:
                        sys.path.insert(0, dirpath)

    def add_extensions(self):
        """add extended functionalities into application environment."""

        # add mini-mo basic extensions
        self.__ext = importlib.import_module("minimo.ext")

        if self.root_path is not None and \
            os.path.exists(os.path.join(self.root_path, "ext")):
            # add project instance related extensions
            self.__ext.__dict__.update(importlib.import_module("ext").__dict__)

    @staticmethod
    def parse_cli():
        """parse cli to get options"""

        argv = sys.argv[:]
        argv.pop(0)
        options = { "cmd": argv.pop(0) }

        index = 0
        while index < len(argv):
            arg = argv[index]

            # check out options
            if "-" == arg[0]:
                k = re.sub("^-+", "", argv.pop(index))

                # check out parameter
                if index < len(argv) and argv[index][0] != "-":
                    options[k] = argv.pop(index)
                else:
                    options[k] = True
            else:
                index += 1

        options["args"] = argv                  
        return options
# end
