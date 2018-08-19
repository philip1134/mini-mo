# -*- coding:utf-8 -*-


__version__ = "0.3.0.b1"


import os
import runpy
from .app import MoApplication
from .performer import MoPerformer
from .callbacks import before_action, action_step, after_action
from .helpers import *


def main():
    bin_path = os.path.join(os.getcwd(), "bin", "minimo")
    if os.path.exists(bin_path):
        runpy.run_path(bin_path)
    else:
        from minimo import MoApplication
        MoApplication().main()

# end
