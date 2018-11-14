# -*- coding:utf-8 -*-


__version__ = "0.3.1.b3"


import os
import runpy
from .app import Application
from .performer import Performer
from .callbacks import before_action, action_step, after_action
from .helpers import *


def main():
    bin_path = os.path.join(os.getcwd(), "bin", "minimo")
    if os.path.exists(bin_path):
        runpy.run_path(bin_path)
    else:
        from minimo import Application
        Application().main()

# end
