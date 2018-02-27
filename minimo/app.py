# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import gettext 
from .globals import *
from .helpers import *
from .generator import *
from .commands import *


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
            if g.routes.has_key(cmd):
                g.routes[cmd]["handler"](_options)
            else:
                error(_("error.unrecognized_command"))
        except:
            error(_("error.wrong_usage"))
            print format_traceback() 

    @staticmethod
    def parse_cli():
        """parse cli to get options"""

        argv = sys.argv[:]
        argv.pop(0)
        options = { "cmd": argv.pop(0) }

        if "-a" in argv:
            index_author = argv.index("-a")
            argv.pop(index_author)
            options["author"] = argv.pop(index_author)

        options["args"] = argv                  

        return options
# end
