# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2019-01-29
#


import collections
from .timer import Timer


class Counter(collections.OrderedDict):
    """counter to count error/warning/exception/success/failure
    in the task process.
    """

    ERROR = "error"
    WARNING = "warning"
    EXCEPTION = "exception"
    SUCCESS = "success"
    FAILURE = "failure"
    TIMER = "timer"

    MINIMO = "__minimo_application__"

    def __init__(self):
        super(Counter, self).__init__()

        # count application informations respectively
        self._app = {
            self.ERROR: None,
            self.EXCEPTION: None,
            self.WARNING: None,
            self.SUCCESS: None,
            self.FAILURE: None,
            self.TIMER: None
        }

    def length(self):
        """get map lenght"""

        return len(self)

    def keys(self):
        """override keys() due to different odict keys()/values() type between
        python2 and python3."""

        return list(super(Counter, self).keys())

    def values(self):
        """override values() due to different odict keys()/values() type
        between python2 and python3."""

        return list(super(Counter, self).values())

    def get(self, key, flag):
        """get key's values"""

        if key in self:
            return self[key].get(flag)
        else:
            return None

    def append(self, key, flag, value):
        """append value to the key"""

        if key not in self:
            self[key] = self.__get_initialized_data()

        self[key][flag].append(value)

    def start_timer_for(self, key):
        """start timer to count duration for the specified key (task-case)."""

        if key not in self:
            self[key] = self.__get_initialized_data()

        self[key][self.TIMER] = Timer("counter_timer_%s" % key)

    def start_timer_for_app(self):
        """start timer for the application to count the whole task duration."""

        self._app[self.TIMER] = Timer("counter_timer_%s" % self.MINIMO)

    def stop_timer_for(self, key):
        """stop timer for the specified key (task-case)."""

        self[key][self.TIMER].stop()

    def stop_timer_for_app(self):
        """stop timer for the application."""

        self._app[self.TIMER].stop()

    def get_duration_of(self, key):
        """get timer counted duration of the specified key (task-case)."""

        if key in self and self[key][self.TIMER] is not None:
            return self[key][self.TIMER].duration()
        else:
            return 0

    def get_duration_of_app(self):
        """get timer counted duration of the application."""

        return self._app[self.TIMER].duration()

    def count_flag(self, flag, force_count=False):
        """count total number for the specified flag"""

        if force_count or self._app.get(flag) is None:
            count = 0
            for key, value in self.items():
                count += len(value[flag])

            self._app[flag] = count

        return self._app[flag]

# private
    def __get_initialized_data(self):
        """generate initialized data"""

        return {
            self.ERROR: [],
            self.EXCEPTION: [],
            self.WARNING: [],
            self.SUCCESS: [],
            self.FAILURE: [],
            self.TIMER: None
        }


def make_append_method(flag):
    def _append(self, key, value):
        self.append(key, flag, value)
    return _append


def make_get_method(flag):
    def _get(self, key):
        return self.get(key, flag)
    return _get


def make_count_method(flag):
    def _count(self, force_count=False):
        return self.count_flag(flag, force_count)
    return _count


for flag in (
    Counter.ERROR,
    Counter.EXCEPTION,
    Counter.WARNING,
    Counter.SUCCESS,
    Counter.FAILURE
):
    _append = make_append_method(flag)
    _get = make_get_method(flag)
    _count = make_count_method(flag)
    _name = flag.lower()
    setattr(Counter, "append_%s" % _name, _append)
    setattr(Counter, "get_%s" % _name, _get)
    setattr(Counter, "total_%s" % _name, _count)

# end
