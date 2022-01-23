# -*- coding:utf-8 -*-


__version__ = "0.8.6"


import os
import runpy
from minimo.app import Application
from minimo.performer import Performer
from minimo.callbacks import before, step, after, \
    before_action, action_step, after_action
from minimo.utils import *
from minimo.attribute_dict import AttributeDict, SimpleAttributeDict
from minimo.logger import Logger


def main():
    bin_path = os.path.join(os.getcwd(), "bin", "minimo")
    if os.path.exists(bin_path):
        runpy.run_path(bin_path)
    else:
        Application().main()

# end
