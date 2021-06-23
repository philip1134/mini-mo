# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import click
from ..utils import *
from minimo import __version__


@click.command("version")
def print_version():
    """print minimo version number.

    usage in cli mode:

        $ mmo version

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api",
                    root_path=instance_project_path)

        # version string
        version = mmo.call("version")
    """

    version = "minimo {}".format(__version__)

    info(version)
    return version


# end
