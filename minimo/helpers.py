# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-09
#

import re
import traceback

TRACE_SPLITTER = "*" * 50

def format_duration(time):
    """format duration, unit of input time should be 'second'"""
    fmt = ""
    if time < 1:
        fmt = _("format.time.ms").format(time * 1000)
    elif time >= 1 and time < 60:
        # seconds
        fmt = _("format.time.second").format(time)
    elif time >= 60 and time < 3600:
        # minutes and seconds
        min = int(time / 60)
        sec = time - min * 60
        fmt = _("format.time.minute").format(min, sec)
    elif time >= 3600 and time < 86400:
        # hours, minutes and seconds
        hour = int(time / 3600)
        min = int((time - hour * 3600) / 60)
        sec = time - hour * 3600 - min * 60
        fmt = _("format.time.hour").format(hour, min, sec)
    else:
        # days, hours, minutes and seconds
        day = int(time / 86400)
        hour = int((time - day * 86400) / 3600)
        min = int((time - day * 86400 - hour * 3600) / 60)
        sec = time - day * 86400 - hour * 3600 - min * 60
        fmt = _("format.time.day").format(day, hour, min, sec)
    return fmt

def format_traceback():
    """format traceback message"""
    tb = "{splitter}\n{traceback}\n{splitter}\n".format(\
        splitter = TRACE_SPLITTER, traceback = traceback.format_exc())
    return unicode(tb, "utf-8")

def upperfirst(value):
    """upper first word of string, and does not change the rest case,
    such as:
        foobAr => FoobAr
    """
    if len(value) > 0:
        return value[0].upper() + value[1:]
    else:
        return value[0].upper()

def camelize(value):
    """convert string to camelcase, will split string by '_' and 
    capitalize the followed word, such as:
        foo_bar => FooBar
    """
    return upperfirst(re.sub(r'(?!^)_([a-zA-Z])', \
        lambda m: m.group(1).upper(), value))

def underscore(value):
    """convert string to underscore case, will split string by capitalized
    word and replaced by '_' + lowercase, such as:
        FooBar => foo_bar
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def validate_keys(targets, keys):
    """check out keys exist in targets or not, targets should be a dict, \
    and keys is a dict contains key:error_message pairs"""
    result = True
    for key, msg in keys.items():
        if not targets.has_key(key):
            error(msg)
            result = False
            # don't break here, check all the items once.
    return result

def info(message, *args, **kwargs):
    print message.format(*args, **kwargs)

def warning(message, *args, **kwargs):
    print u"(!) WARNING " + message.format(*args, **kwargs)

def error(message, *args, **kwargs):
    print u"(x) ERROR " + message.format(*args, **kwargs)