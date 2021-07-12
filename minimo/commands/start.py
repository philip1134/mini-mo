# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-02-26
#

import click
from ..globals import ctx
from ..utils import *
from ..scheduler import Scheduler
from .common import verify_root_path
from .run import run_suite_with_context


@click.command("start")
def start_scheduler():
    """start scheduler.

    usage in cli mode:

        $ mmo start

    ----------

    usage in api mode:

        import minimo

        mmo = minimo.Application(
                    interface="api",
                    root_path=instance_project_path)

        result = mmo.call("start")
    """

    if not verify_root_path(ctx):
        return False

    scheduler = Scheduler(
        run_suite_with_context,
        ctx
    )
    scheduler.run()

# end
