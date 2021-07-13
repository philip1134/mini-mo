# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-09
#

import re
import traceback
import click
import collections
# import threading


TRACE_SPLITTER = "*" * 50


def format_duration(time):
    """format duration, unit of input time should be 'second'."""

    fmt = ""
    if time < 1:
        fmt = "{:.3f} ms".format(time * 1000)
    elif time >= 1 and time < 60:
        # seconds
        fmt = "{:.3f} sec".format(time)
    elif time >= 60 and time < 3600:
        # minutes and seconds
        min = int(time / 60)
        sec = time - min * 60
        fmt = "{:d} min {:.3f} sec".format(min, sec)
    elif time >= 3600 and time < 86400:
        # hours, minutes and seconds
        hour = int(time / 3600)
        min = int((time - hour * 3600) / 60)
        sec = time - hour * 3600 - min * 60
        fmt = "{:d} hour {:d} min {:.3f} sec".format(hour, min, sec)
    else:
        # days, hours, minutes and seconds
        day = int(time / 86400)
        hour = int((time - day * 86400) / 3600)
        min = int((time - day * 86400 - hour * 3600) / 60)
        sec = time - day * 86400 - hour * 3600 - min * 60
        fmt = "{:d} day {:d} hour {:d} min {:.3f} sec".format(day, hour,
                                                              min, sec)
    return fmt


def format_traceback():
    """format traceback message."""

    return "{splitter}\n{traceback}\n{splitter}\n".format(
        splitter=TRACE_SPLITTER, traceback=traceback.format_exc())


def upperfirst(value):
    """upper first word of string, and does not change the rest case,
    such as:
        foobAr => FoobAr
    """

    if len(value) > 1:
        return value[0].upper() + value[1:]
    else:
        return value[0].upper()


def camelize(value):
    """convert string to camelcase, will split string by '_' and
    capitalize the followed word, such as:
        foo_bar => FooBar
    """

    return upperfirst(re.sub(r'(?!^)_([a-zA-Z])',
                      lambda m: m.group(1).upper(), value))


def underscore(value):
    """convert string to underscore case, will split string by capitalized
    word and replaced by '_' + lowercase, such as:
        FooBar => foo_bar
    """

    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def flatten(l):
    """make list flatten"""

    for el in l:
        try:
            is_basestring = isinstance(el, basestring)
        except NameError:
            is_basestring = isinstance(el, str)

        if isinstance(el, collections.Iterable) and not is_basestring:
            for sub in flatten(el):
                yield sub
        else:
            yield el


def convert_newline(value):
    """convert CR-LF to unix-like new line as LF"""

    return re.sub(r"\r\n", r"\n", value)


def info(message):
    """print normal message in stdout."""

    click.echo(message)


def stage(message):
    """print stage message in stdout."""

    click.secho(message, fg="green")


def warning(message):
    """print warning message in stdout."""

    click.secho("[WARNING] " + message, fg="yellow")


def error(message):
    """print error message in stdout."""

    click.secho("[ERROR] " + message, fg="red")

# end
