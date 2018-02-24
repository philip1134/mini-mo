# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-09
#

import traceback

TRACE_SPLITTER = "*" * 50

def format_duration(time):
    """格式化持续时间，输入time单位为秒"""
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
    """格式化traceback信息"""
    tb = TRACE_SPLITTER + "\n" \
        + traceback.format_exc() \
        + TRACE_SPLITTER + "\n"
    return unicode(tb, "utf-8")

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