# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#

import time

class Timer(object):
    """timer, started at initialized."""

    timers = {}

    def __init__(self, name):
        self.started_at = time.time()
        self.name = name

        Timer.timers[name] = self

    def duration(self):
        """calculate duration started from timer initialized. unit is sec."""
        return time.time() - self.started_at

    @classmethod
    def get(cls, name):
        """get named timer with {name}"""
        return cls.timers[name]
# end
