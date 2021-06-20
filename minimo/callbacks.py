# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#
# export:
#   callbacks
#   before_action
#   action_step
#   after_action
#

import inspect
from functools import wraps
from .globals import ctx


class Callbacks:
    """object to store defined callbacks.
    """

    def __init__(self):
        super(Callbacks, self).__init__()

        self.before_action_funcs = {}
        self.after_action_funcs = {}
        self.action_step_funcs = {}

    def clear_before_action(self, key):
        """clear before_action filters"""

        self.before_action_funcs[key] = []

    def clear_after_action(self, key):
        """clear after_action filters"""

        self.after_action_funcs[key] = []

    def append_to_before_actions(self, key, value):
        """append function to before_action filters"""

        self._append_to(key, value, self.before_action_funcs)

    def get_before_actions(self, key):
        """get before_action filters, return an empty array if there's
        no function in filter list.
        """

        if key in self.before_action_funcs:
            return self.before_action_funcs[key]
        else:
            return []

    def append_to_action_steps(self, key, value):
        """append function to action_step list"""

        self._append_to(key, value, self.action_step_funcs)

    def get_action_steps(self, key):
        """get action_step list, return an empty array if there's
        no function in that list.
        """

        if key in self.action_step_funcs:
            return self.action_step_funcs[key]
        else:
            return []

    def append_to_after_actions(self, key, value):
        """append function to after_action filters"""

        self._append_to(key, value, self.after_action_funcs)

    def get_after_actions(self, key):
        """get after_action filters, return an empty array if there's
        no function in filter list.
        """

        if key in self.after_action_funcs:
            return self.after_action_funcs[key]
        else:
            return []

    def _append_to(self, key, value, container):
        """append value to container by key"""

        if key in container:
            container[key].append(value)
        else:
            container[key] = [value]


ctx.callbacks = Callbacks()


def _get_caller_id_by_frame(caller):
    return "%s.%s" % (caller.f_locals["__module__"],
                      caller.f_code.co_name)


def before_action(*params):
    """to specify the action will be executed before task."""

    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        ctx.callbacks.append_to_before_actions(
            _get_caller_id_by_frame(inspect.currentframe().f_back),
            decorated_func)
        return decorated_func
    return decorator


def after_action(*params):
    """to specify the action will be executed after task."""

    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        ctx.callbacks.append_to_after_actions(
            _get_caller_id_by_frame(inspect.currentframe().f_back),
            decorated_func)
        return decorated_func
    return decorator


def action_step(*params):
    """to specify the action is one task step.
    the specified action should return True or False to
    represent success or failure of that task step.
    """

    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        ctx.callbacks.append_to_action_steps(
            _get_caller_id_by_frame(inspect.currentframe().f_back),
            decorated_func)
        return decorated_func
    return decorator

# end
