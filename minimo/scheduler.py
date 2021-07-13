# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


import copy
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.executors.pool import ProcessPoolExecutor
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

        if self._configured and self._init_jobs():
            self.start()

# protected
    def _load_config(self, config):
        """load scheduler configuration"""

        # flag
        self._configured = True

        if isinstance(config, dict) and "scheduler" in config:
            self.config = copy.deepcopy(config["scheduler"])

            # jobstore
            if "jobstore" in self.config:
                try:
                    jobstore = self.config["jobstore"]
                    self.add_jobstore(
                        jobstore.pop("type"),
                        **jobstore
                    )
                except Exception:
                    error("invalid jobstore configuration.")
                    info(format_traceback())
                    self._configured = False

            # executor
            if "executor" in self.config:
                max_workers = self.config["executor"].get("max_workers", 1)
            else:
                max_workers = 1

            self.add_executor(
                ProcessPoolExecutor(max_workers),
                "default"
            )

        else:
            warning("no scheduler configured.")
            self._configured = False
            self.config = None

    def _init_jobs(self):
        """initialize jobs and add them to scheduler"""

        if isinstance(self.config, dict) and "jobs" in self.config:
            info("initializing jobs...")

            for job_config in self.config["jobs"]:
                case = job_config["case"]
                job_id = job_config.get("id", case)

                if job_config.get("enable", True):
                    info("add job '%s'" % job_id)

                    self.add_job(
                        self.job_func,
                        id=job_id,
                        name=case,
                        kwargs={
                            "cases": case,
                        },
                        replace_existing=True,
                        max_instances=1,
                        executor="default",
                        **job_config["config"]
                    )
                else:
                    info("skip job '%s' due to be disabled" % job_id)

            return True
        else:
            warning("no scheduled job configured.")
            return False

# end
