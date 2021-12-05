<%text># -*- coding:utf-8 -*-</%text>


import os
from minimo import before, step, after
from lib import BasePerformer


__author__ = "${author}"
__date__ = "${date}"


class Performer(BasePerformer):
    """docstring for Performer"""

    def __init__(self):
        super(Performer, self).__init__(
            name="${case_name}",
            case_path=os.path.abspath(__file__)
        )

        # add initializing code here

    @before()
    def setUp(self):
        """set up env"""

        pass

    @after()
    def tearDown(self):
        """tear down"""

        pass

    @step()
    def first_action(self):
        """first step description"""

        # your step code here

        # True for success, otherwise False
        return True

#    @step()
#    def second_action(self):
#        """second step description"""
#
#        # your step code here
#
#        return True


# end
