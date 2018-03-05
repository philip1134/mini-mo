# -*- coding:utf-8 -*-
"""
    minimo.__main__

    Alias for minimo.run for the command line.
"""

import os
import runpy

def main():
    bin_path = os.path.join(os.getcwd(), "bin", "minimo")
    if os.path.exists(bin_path):
        runpy.run_path(bin_path)
    else:
        from minimo import MoApplication
        MoApplication().run()    

if "__main__" == __name__:
    main()