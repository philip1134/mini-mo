# -*- coding:utf-8 -*-


__version__ = "0.6.1"


import os
import runpy
from .app import Application
from .performer import Performer
from .callbacks import before_action, action_step, after_action
from .helpers import *
from .attribute_dict import AttributeDict
from .logger import Logger
from .ext import copy_template_file, copy_template_folder


def main():
    bin_path = os.path.join(os.getcwd(), "bin", "minimo")
    if os.path.exists(bin_path):
        runpy.run_path(bin_path)
    else:
        Application().main()

# end
