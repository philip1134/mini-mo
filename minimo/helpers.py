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
        fmt = "%.3f 毫秒"%(time * 1000)
    elif time >= 1 and time < 60:
        # seconds
        fmt = "%.3f 秒"%time
    elif time >= 60 and time < 3600:
        # minutes and seconds
        min = int(time / 60)
        sec = time - min * 60
        fmt = "%d 分 %.3f 秒"%(min, sec)
    elif time >= 3600 and time < 86400:
        # hours, minutes and seconds
        hour = int(time / 3600)
        min = int((time - hour * 3600) / 60)
        sec = time - hour * 3600 - min * 60
        fmt = "%d 小时 %d 分 %.3f 秒"%(hour, min, sec)
    else:
        # days, hours, minutes and seconds
        day = int(time / 86400)
        hour = int((time - day * 86400) / 3600)
        min = int((time - day * 86400 - hour * 3600) / 60)
        sec = time - day * 86400 - hour * 3600 - min * 60
        fmt = "%d 天 %d 小时 %d 分 %.3f 秒"%(day, hour, min, sec)
    return fmt

def format_traceback():
    """format traceback message"""
    tb = TRACE_SPLITTER + "\n" \
        + traceback.format_exc() \
        + TRACE_SPLITTER + "\n"
    return unicode(tb, "utf-8")

def camelize(value):
    """convert string to camelcase, will split string by '_' and 
    capitalize the followed word, such as:
        foo_bar => FooBar
    """
    def camelcase(): 
        yield str.lower
        while True:
            yield str.capitalize

    c = camelcase()
    return "".join(c.next()(x) if x else '_' for x in value.split("_"))

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
    return result

def info(message, *args, **kwargs):
    print message.format(*args, **kwargs)

def warning(message, *args, **kwargs):
    print u"(!) 警告： " + message.format(*args, **kwargs)

def error(message, *args, **kwargs):
    print u"(x) 错误： " + message.format(*args, **kwargs)