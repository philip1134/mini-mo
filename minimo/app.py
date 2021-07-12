# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#

import os
import sys
import importlib
import yaml
import logging
from .globals import ctx
from .interface import InterfaceFactory
from .utils import *
from .reporter import Reporter
from .logger import StdoutToFileLogger


class Application:
    """the Application object implements the basic entry of
    minimo framework.
    """

    # project name, set in project instance
    name = "minimo"

    # report format type, supported "text", "html" and "xml",
    # default is "html"
    #   text: plain text
    #   html: html web page
    #   xml: xml file, can be recognized by most CI system
    # output = "text"

    # case running type, should be "serial" or "concorrence",
    # default is "serial"
    #   serial: run cases one by one
    #   concorrence: run cases concorrently by threads.
    # running_type = "serial"

    # redirect stdout message to log file or not.
    # if running in background, there maybe raises exception due to no stdout
    # handler, so set this flag to True, print stdout message to log file.
    # it is forced to redirection under api mode.
    # redirect_stdout_to_file = False

    # project modules path, which will be inserted into sys.path at application
    # started. by default, "lib", "ext", "cases", "vendor" will be added
    # mandatory.
    mandatory_modules_path = ["lib", "ext", "cases", "vendor"]
    modules_path = []

    def __init__(self, **attrs):
        super(Application, self).__init__()

        # root path of project instance
        self.inst_path = attrs.pop("root_path", None)

        # flags intializing
        self._loaded_modules_path = False

        # project interface, supported "cli", "api", default is "cli"
        #   cli: call commands/functions as command line interface
        #   api: call commands/functions as api
        self.interface = attrs.pop("interface", "cli")
        self._interf = InterfaceFactory.get(
            self.interface, **attrs)

        # load plugins and extensions
        self._load_plugins()
        self._load_extensions()

        # load config from yaml under project instance's root_path
        self._load_config()

        # ctx.app = self

    def run(self, *args, **kwargs):
        """alias for :meth:`main`."""

        self.main(*args, **kwargs)

    def call(self, *args, **kwargs):
        """alias for :meth:`main`."""

        self.main(*args, **kwargs)

    def main(self, *args, **kwargs):
        """main function entry"""

        self._setup()

        result = self._interf.main(*args, **kwargs)

        self._teardown()

        return result

    def get_command(self, context, name):
        """wrapper for get_command"""

        return self._interf.get_command(self, context, name)

    def list_commands(self, context):
        """wrapper for list_command"""

        return sorted(
            set(self._interf.list_commands(self, context))
        )

    def is_cli_mode(self):
        return "cli" == self.interface

    def is_api_mode(self):
        return "api" == self.interface

    def echo_to_file(self):
        """check out if print console message to file"""

        return ctx.config.redirect_stdout_to_file or self.is_api_mode()

    def echo_to_stdout(self):
        """check out if print console message to stdout"""

        return not self.echo_to_file()

# protected
    def _setup(self):
        """setup runtime environment"""

        # initialize runtime context
        self._init_context()

        # start timer for the application
        ctx.counter.start_timer_for_app()

        # add modules path to sys.path
        self._add_modules_path()

    def _teardown(self):
        """tear down runtime environment"""

        # stop timer for the application
        ctx.counter.stop_timer_for_app()

    def _load_config(self):
        """load project configurations: config.yml"""

        if self.inst_path is not None:
            config_path = os.path.join(self.inst_path, "config.yml")
            if self.inst_path is not None and os.path.exists(config_path):
                with open(config_path, mode="r", encoding="utf-8") as f:
                    # load yml to config and app attributes
                    cfg = yaml.full_load(f.read())
                    if isinstance(cfg, dict):
                        ctx.config.update(cfg)
                        ctx.app.update({
                            "name": self.name,
                            "inst_path": self.inst_path,
                            "interface": self.interface,
                            "is_cli_mode": self.is_cli_mode(),
                            "is_api_mode": self.is_api_mode(),
                            "echo_to_file": self.echo_to_file(),
                            "echo_to_stdout": self.echo_to_stdout(),
                        })

    def _init_context(self):
        """initialize runtime context"""

        ctx.reporter = Reporter()

        if self.echo_to_file():
            # redirect stdout to log file
            self._logger = StdoutToFileLogger(
                name="stdout",
                output_path=os.path.join(self.inst_path, "log"),
                outputs={
                    "fulltrace": logging.DEBUG
                }
            )

            sys.stdout = self._logger

    def _add_modules_path(self):
        """walk through modules_path, if there's __init__.py, the folder will
        be added into sys.path.
        """

        if self._loaded_modules_path \
           or self.inst_path is None:
            return

        # add instance path to sys.path
        sys.path.insert(0, self.inst_path)

        for target in set(self.modules_path + self.mandatory_modules_path):
            target_dir = os.path.join(self.inst_path, target)
            if os.path.exists(target_dir):
                for dirpath, dirs, files in os.walk(target_dir):
                    if "__init__.py" in files:
                        sys.path.insert(0, dirpath)

        self._loaded_modules_path = True

    def _load_plugins(self):
        """load plugins which were registered as 'minimo.commands'."""

        try:
            import pkg_resources
        except ImportError:
            return

        for ep in pkg_resources.iter_entry_points('minimo.commands'):
            self._interf.add_command(ep.load(), ep.name)

    def _load_extensions(self):
        """load extensions for minimo style project. such extensions will be
        placed under project/ext folder, as minimo does, add the extended
        commands to __autoload__ tuple, and minimo will load them
        automatically.
        """

        if self.inst_path is not None \
           and os.path.exists(os.path.join(self.inst_path, "ext")):
            try:
                for cmd in importlib.import_module("ext").__autoload__:
                    self._interf.add_command(cmd)
            except Exception:
                # do nothing
                return

# end
