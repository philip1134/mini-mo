# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import os
from ..globals import g
from ..helpers import *
from ..route import register
from minimo import __version__


@register("version", "help.version", True)
def minimo_print_version(*args):
    """print minimo version number."""
    info("minimo {}".format(__version__))


@register("help", "help.help", True)
def minimo_print_usage(*args):
    """show help information."""

    sub_commands = ""
    for cmd, conf in g.routes.items():
        if conf["trans"]:
            _help = _(conf["help"])
        else:
            _help = conf["help"]
        prefix, _cmd = cmd.split(":")
        if prefix == "minimo" or prefix == g.app.type:
            sub_commands += "\n* {0} - {1}\n".format(_cmd, _help)

    info(_("help.app"),
        project_name = g.app.name,
        sub_commands = sub_commands)

