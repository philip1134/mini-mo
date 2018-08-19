# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2018-08-18
#


import click


class InterfaceFactory:
    """factory to create interface"""

    @classmethod
    def get(cls, type, **attrs):
        """get interface instance by type"""

        if "api" == type:
            return MoApi(**attrs)
        else:
            return click.Group(**attrs)


class MoApi(object):
    """Interface for api type"""

    def __init__(self, **attrs):
        super(MoApi, self).__init__()

        # initialize command mapper
        self.commands = attrs.get("commands") or {}

    def main(self, prog_name, **kwargs):
        return self.commands[prog_name](**kwargs)

    def add_command(self, cmd, name=None):
        """register command name and handler to command mapper."""

        name = name or cmd.name
        if name is None:
            raise TypeError('Command has no name.')
        self.commands[name] = cmd

    def get_command(self, ctx, name):
        return self.commands.get(name)

    def list_commands(self, ctx):
        return sorted(self.commands)

# end
