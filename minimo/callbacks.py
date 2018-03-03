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
from .globals import g

class Callbacks(object):
    def __init__(self):
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
        self.__append_to(key, value, self.before_action_funcs)
        
    def get_before_actions(self, key):
        """get before_action filters, return an empty array if there's
        no function in filter list."""
        if self.before_action_funcs.has_key(key):
            return self.before_action_funcs[key]
        else:
            return []
        
    def append_to_action_steps(self, key, value):
        """append function to action_step list"""
        self.__append_to(key, value, self.action_step_funcs)    
        
    def get_action_steps(self, key):  
        """get action_step list, return an empty array if there's
        no function in that list."""  
        if self.action_step_funcs.has_key(key):
            return self.action_step_funcs[key]
        else:
            return []
        
    def append_to_after_actions(self, key, value):
        """append function to after_action filters"""
        self.__append_to(key, value, self.after_action_funcs)
        
    def get_after_actions(self, key): 
        """get after_action filters, return an empty array if there's
        no function in filter list."""  
        if self.after_action_funcs.has_key(key):
            return self.after_action_funcs[key]
        else:
            return []
        
    def __append_to(self, key, value, list):
        if list.has_key(key):
            list[key].append(value)
        else:
            list[key] = [value]
        
g.callbacks = Callbacks()

def __get_caller_id_by_frame(caller):
    return "{0}.{1}".format(caller.f_locals["__module__"], caller.f_code.co_name)

def before_action(desc):
    """to specify the action will be executed before task."""
    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        f.__desc__ = decorated_func.__desc__ = desc
        g.callbacks.append_to_before_actions(\
            __get_caller_id_by_frame(inspect.currentframe().f_back), \
            decorated_func)
        return decorated_func
    return decorator

def after_action(desc):
    """to specify the action will be executed after task."""
    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        f.__desc__ = decorated_func.__desc__ = desc
        g.callbacks.append_to_after_actions(\
            __get_caller_id_by_frame(inspect.currentframe().f_back), \
            decorated_func)
        return decorated_func
    return decorator

def action_step(desc):
    """to specify the action is one task step. 
    the specified action should return True or False to
    represent success or failure of that task step."""
    def decorator(f):
        @wraps(f)
        def decorated_func(self, *args, **kwargs):
            return f(self, *args, **kwargs)
        f.__desc__ = decorated_func.__desc__ = desc
        g.callbacks.append_to_action_steps(\
            __get_caller_id_by_frame(inspect.currentframe().f_back), \
            decorated_func)
        return decorated_func
    return decorator
        