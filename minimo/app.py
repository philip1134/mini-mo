# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-10
#

import os
import sys
import importlib
from .ext import __autoload__
from .interface import InterfaceFactory
from .globals import g, GLOBAL_NS
from .helpers import *


class Application(object):
    """the MoApplication object implements the basic entry of
    minimo framework.
    """

    # project name, set in project instance
    name = "minimo"

    # project type, default is "minimo"
    type = GLOBAL_NS

    # project root path, auto set in project instance
    root_path = None

    # project interface, supported "cli", "api", default is "cli"
    #   cli: call commands/functions as command line interface
    #   api: call commands/functions as api
    interface = "cli"

    # report format type, supported "text", "html" and "xml",
    # default is "html"
    #   text: plain text
    #   html: html web page
    #   xml: xml file, can be recognized by most CI system
    output = "html"

    # case running type, should be "serial" or "concorrence",
    # default is "serial"
    #   serial: run cases one by one
    #   concorrence: run cases concorrently by subprocess.
    run_cases = "serial"

    # project modules path, which will be inserted into sys.path at application
    # started. by default, "lib", "ext", "cases", "vendor" will be added
    # mandatory.
    mandatory_modules_path = ["lib", "ext", "cases", "vendor"]
    modules_path = []

    def __init__(self, **attrs):
        super(Application, self).__init__()

        self._loaded_plugins = \
            self._loaded_extensions = \
            self._loaded_modules_path = False

        self.__interface = InterfaceFactory.get(self.interface, **attrs)

        # add default cli
        for cli in __autoload__:
            self.__interface.add_command(cli)

        g.app = self

    def run(self, *args, **kwargs):
        """alias for :meth:`main`."""
        self.main(*args, **kwargs)

    def main(self, *args, **kwargs):
        # main function entry, we just load modules path to sys.path before
        # app running up
        self._add_modules_path()

        return self.__interface.main(*args, **kwargs)

    def get_command(self, ctx, name):
        # We load plugins and extension with built-in commands as these should
        # always be the same no matter what the app does.
        self._load_plugins()
        self._load_extensions()

        return self.__interface.get_command(self, ctx, name)

    def list_commands(self, ctx):
        # we always load plugins and extensions with minimo builtin commands.
        self._load_plugins()
        self._load_extensions()

        rv = set(self.__interface.list_commands(self, ctx))
        return sorted(rv)

    def _add_modules_path(self):
        """walk through modules_path, if there's __init__.py, the folder will
        be added into sys.path
        """

        if self._loaded_modules_path or self.root_path is None:
            return

        for target in set(self.modules_path + self.mandatory_modules_path):
            target_dir = os.path.join(self.root_path, target)
            if os.path.exists(target_dir):
                for dirpath, dirs, files in os.walk(target_dir):
                    if "__init__.py" in files:
                        sys.path.insert(0, dirpath)

        self._loaded_modules_path = True

    def _load_plugins(self):
        """load plugins which were registered as 'minimo.commands'."""

        if self._loaded_plugins:
            return

        try:
            import pkg_resources
        except ImportError:
            self._loaded_plugins = True
            return

        for ep in pkg_resources.iter_entry_points('minimo.commands'):
            self.__interface.add_command(ep.load(), ep.name)
        self._loaded_plugins = True

    def _load_extensions(self):
        """load extensions for minimo style project. such extensions will be
        placed under project/ext folder, as minimo does, add the extended
        commands to __autoload__ tuple, and minimo will load them
        automatically.
        """

        if self._loaded_extensions:
            return

        if self.root_path is not None \
           and os.path.exists(os.path.join(self.root_path, "ext")):
            try:
                for cli in importlib.import_module("ext").__autoload__:
                    self.__interface.add_command(cli)
            except Exception:
                # do nothing
                self._loaded_extensions = True
                return
        self._loaded_extensions = True
# end
