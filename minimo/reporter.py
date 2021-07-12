# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2019-01-29
#


import os
from mako.template import Template
from .globals import ctx, BLOCK_SPLITTER
from .utils import *


class Reporter:
    """print report to file according to output type, currently support
    'text', 'xml', 'html'.
    """

    def __init__(self):
        super(Reporter, self).__init__()

        self.output_path = None

    def report(self):
        """print report to file according to output type."""

        try:
            self.summary = (
                'mission completed in %s\n'
                'totally %d cases were executed with:\n'
                '    %d warning, %d error, %d exception\n'
                '    %d success, %d failure' % (
                    format_duration(ctx.counter.get_duration_of_app()),
                    ctx.counter.length(),
                    ctx.counter.total_warning(),
                    ctx.counter.total_error(),
                    ctx.counter.total_exception(),
                    ctx.counter.total_success(),
                    ctx.counter.total_failure()))

            if ctx.app.is_cli_mode:
                self._print_to_stdout(ctx.counter)

            # print to file
            if ctx.config.output in ("text", "xml", "html") \
               and ctx.output_path is not None \
               and os.path.exists(ctx.output_path):

                self.output_path = getattr(
                    self, "_print_to_%s" % ctx.config.output)(
                    ctx.output_path, ctx.counter)

                stage("\nreport in:\n%s" % self.output_path)
        except Exception:
            error("error occured in reporting:\n%s" % format_traceback())
        finally:
            return self.output_path

# protected
    def _print_to_stdout(self, counter):
        """print summary to stdout"""

        stage('\n\n%s' % BLOCK_SPLITTER)
        stage(self.summary)

    def _print_to_text(self, path, counter):
        """print report to text file"""

        file_path = os.path.join(path, "report.txt")

        content = Template(
            filename=os.path.join(ctx.minimo_root_path,
                                  "templates",
                                  "reports",
                                  "report.txt.mako")
        ).render_unicode(
            suite_name=ctx.suite_name,
            summary=self.summary,
            counter=counter)

        with open(file_path, "w") as f:
            f.write(convert_newline(content))

        return file_path

    def _print_to_xml(self, path, counter):
        """print report to xml file"""

        file_path = os.path.join(path, "report.xml")

        content = Template(
            filename=os.path.join(ctx.minimo_root_path,
                                  "templates",
                                  "reports",
                                  "report.xml.mako"),
        ).render_unicode(
            suite_name=ctx.suite_name,
            counter=counter)

        with open(file_path, "w") as f:
            f.write(convert_newline(content))

        return file_path

    def _print_to_html(self, path, counter):
        """print report to html file"""

        file_path = os.path.join(path, "report.html")

        content = Template(
            filename=os.path.join(ctx.minimo_root_path,
                                  "templates",
                                  "reports",
                                  "report.html.mako"),
        ).render_unicode(
            suite_name=ctx.suite_name,
            counter=counter)

        with open(file_path, "w") as f:
            f.write(convert_newline(content))

        return file_path

# end
