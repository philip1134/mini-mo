# -*- coding:utf-8 -*-


__version__ = "0.8.2"


import os
import runpy
from .app import Application
from .performer import Performer
from .callbacks import before_action, action_step, after_action
from .utils import *
from .attribute_dict import AttributeDict, SimpleAttributeDict
from .logger import Logger


def main():
    bin_path = os.path.join(os.getcwd(), "bin", "minimo")
    if os.path.exists(bin_path):
        runpy.run_path(bin_path)
    else:
        Application().main()

# end
