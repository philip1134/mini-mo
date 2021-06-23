# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-06-20
#


from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler(BackgroundScheduler):
    """scheduler to manage scheduled jobs."""

    def __init__(
        self,
        job_func,
        logger,
        config
    ):
        super(Scheduler, self).__init__()

        self.logger = logger
        self.config = config
        self.job_func = job_func

    def run(self):
        """scheduler main entry"""

        if self._init_jobs():
            self.start()
        else:
            self.logger.error(
                "fail to initialize job. abort to start scheduler.")

# protected
    def _init_jobs(self):
        """initialize jobs and add them to scheduler"""

        result = True

        if (self.config is None) or \
           (self.config.get("jobs", None) is None):
            self.logger.error(
                "no scheduler job configured, skip this work.")
            result = False
        else:
            self.logger.info("initializing jobs...")

            for job_config in self.config["jobs"]:
                case = job_config["case"]
                if job_config.get("enable", True):
                    self.logger.info("add job '%s'" % case)

                    self._jobs[case] = self.add_job(
                        self.job_func,
                        kwargs=job_config.get("params", {}),
                        replace_existing=True,
                        max_instances=1,
                        executor="default",
                        **job_config["config"]
                    )
                else:
                    self.logger.info("job '%s' was disabled" % case)

        return result

# end
