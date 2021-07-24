<%text># -*- coding:utf-8 -*-</%text>


import os
from minimo import before_action, action_step, after_action
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

    @before_action()
    def setUp(self):
        """set up test env"""
        pass

    @after_action()
    def tearDown(self):
        """tear down test"""
        pass

    @action_step()
    def first_action(self):
        """first test step description"""

        # step code

        return True

#    @action_step()
#    def second_action(self):
#        """second test step description"""
#
#        # step code
#
#        return True

# end
