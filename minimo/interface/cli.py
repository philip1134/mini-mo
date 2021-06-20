# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2021-04-27
#


import click


class MoCLI(click.Group):
    """Interface for cli type"""

    def __init__(self, **attrs):
        super(MoCLI, self).__init__()

# end
