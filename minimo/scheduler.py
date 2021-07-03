# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


import copy
from apscheduler.schedulers.blocking import BlockingScheduler
from .utils import *


class Scheduler(BlockingScheduler):
    """scheduler to manage scheduled jobs."""

    def __init__(
        self,
        job_func,
        context
    ):
        super(Scheduler, self).__init__()

        self.job_func = job_func
        self.ctx = context
        self._load_config(self.ctx.config)

    def run(self):
        """scheduler main entry"""

        if self._init_jobs():
            self.start()
        else:
            error("fail to start scheduler.")

# protected
    def _load_config(self, config):
        """load scheduler configuration"""

        if isinstance(config, dict) and "scheduler" in config:
            self.config = copy.deepcopy(config["scheduler"])
        else:
            self.config = None

    def _init_jobs(self):
        """initialize jobs and add them to scheduler"""

        if isinstance(self.config, dict) and "jobs" in self.config:
            info("initializing jobs...")

            for job_config in self.config["jobs"]:
                case = job_config["case"]
                if job_config.get("enable", True):
                    info("add job '%s'" % case)

                    self.add_job(
                        self.job_func,
                        kwargs={
                            "cases": case,
                            "context": self.ctx,
                        },
                        replace_existing=True,
                        max_instances=1,
                        executor="default",
                        **job_config["config"]
                    )
                else:
                    info("skip job '%s' due to be disabled" % case)

            return True
        else:
            error("no scheduler job configured, skip this work.")
            return False

# end
