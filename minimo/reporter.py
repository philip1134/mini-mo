# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2019-01-29
#


import os
from .globals import ctx, BLOCK_SPLITTER, SECTION_SPLITTER
from .helpers import *


class Reporter(object):
    """print report to file according to output type, currently support
    'text', 'xml', 'html'.
    """

    def __init__(self):
        super(Reporter, self).__init__()

    def report(self):
        """print report to file according to output type."""

        self.summary = (
            'mission completed in %s\n'
            'totally %d cases were executed with:\n'
            '    %d warning, %d error, %d exception\n'
            '    %d success, %d failure\n' % (
                format_duration(ctx.counter.get_duration_of_app()),
                len(ctx.counter),
                ctx.counter.total_warning(),
                ctx.counter.total_error(),
                ctx.counter.total_exception(),
                ctx.counter.total_success(),
                ctx.counter.total_failure()))

        if ctx.app.is_cli_mode():
            self._print_to_stdout(ctx.counter)

        if ctx.app.output in ("text", "xml", "html") \
           and ctx.output_path is not None:

            report_path = getattr(self, "_print_to_%s" % ctx.app.output)(
                ctx.output_path, ctx.counter)

            stage("report in:\n%s" % report_path)

# protected
    def _print_to_stdout(self, counter):
        """print summary to stdout"""

        stage('\n\n%s\n' % BLOCK_SPLITTER)
        stage(self.summary)

    def _print_to_text(self, path, counter):
        """print report to text file"""

        file_path = os.path.join(path, "report.txt")

        report = self.summary + "\n\n"

        for case in counter.keys():
            report += "%s\n%s: %s\n\n" % (
                SECTION_SPLITTER,
                case,
                format_duration(counter.get_duration_of(case)))

            for flag in ("error", "exception", "warning"):
                lst = getattr(counter, "get_%s" % flag)(case)
                report += "%s: %d\n" % (flag, len(lst))
                for item in lst:
                    report += "- %s\n" % item
                report += "\n"

        with open(file_path, "w") as f:
            f.write(report)

        return file_path

    def _print_to_xml(self, path, counter):
        """print report to xml file"""

        print ">> here in print to xml"
        file_path = os.path.join(path, "report.xml")

        return file_path

    def _print_to_html(self, path, counter):
        """print report to html file"""

        print ">> here in print to html"
        file_path = os.path.join(path, "report.html")

        return file_path

# end
