# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


from .attribute_dict import SimpleAttributeDict, AttributeDict


# runtime context
class RuntimeContext(SimpleAttributeDict):
    """stores runtime context, includes application information, callbacks,
    test suite name, minimo root path, and etc.
    """

    def __init__(self, defaults={}):
        super(RuntimeContext, self).__init__({
            # application
            "app": AttributeDict({
                # application instance name
                "name": "minimo",

                # application instance path
                "inst_path": None,

                # interface mode, default is `cli`
                "interface": "cli",

                # flags
                "is_cli_mode": True,
                "is_api_mode": False,
                "echo_to_file": False,
                "echo_to_stdout": True,
            }),

            # runtimes
            "counter": None,
            "reporter": None,
            "suite_name": None,
            "output_path": None,

            # global constants
            "callbacks": None,

            # configurations
            "config": AttributeDict({
                # report format type, supported "text", "html" and "xml",
                # default is "text"
                #   text: plain text
                #   html: html web page
                #   xml: xml file, can be recognized by most CI system
                "output": "text",

                # case running type, should be "serial" or "concorrence",
                # default is "serial"
                #   serial: run cases one by one
                #   concorrence: run cases concorrently by threads.
                "running_type": "serial",

                # redirect stdout message to log file or not.
                # if running in background, there maybe raises exception due to
                # no stdout handler, so set this flag to True, print stdout
                # message to log file. it is forced to redirection under
                # api mode.
                "redirect_stdout_to_file": False,
            }),
        })

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)

# end
