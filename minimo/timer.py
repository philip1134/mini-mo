# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#


import time


class Timer:
    """timer, started at initialized."""

    timers = {}

    def __init__(self, name):
        self.started_at = time.time()
        self.name = name
        self._duration = 0
        self._stopped = False

        Timer.timers[name] = self

    def duration(self):
        """calculate duration started from timer initialized. unit is sec."""

        if not self._stopped:
            self._duration = time.time() - self.started_at

        return self._duration

    def stop(self):
        """stop the timer and count the duration"""

        self._duration = time.time() - self.started_at
        self._stopped = True

    @classmethod
    def get(cls, name):
        """get named timer with {name}"""

        return cls.timers[name]
# end
