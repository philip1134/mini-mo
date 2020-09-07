<%text># -*- coding:utf-8 -*-</%text>

__author__ = "${author}"
__date__ = "${date}"


from minimo import before_action, action_step, after_action
from lib import BasePerformer
from . import config


class Performer(BasePerformer):
    """docstring for Performer"""

    def __init__(self):
        super(Performer, self).__init__("${case_name}")
        # add initializing code here

#    @before_action("setting up")
#    def setUp(self):
#        """set up test env"""
#        pass

#    @after_action("tearing down")
#    def tearDown(self):
#        """tear down test"""
#        pass

#    @action_step("step name")
#    def test_first_action(self):
#        """first test step description"""
#
#        # step code
#
#        return True # or False

#    @action_step("step name")
#    def test_second_action(self):
#        """second test step description"""
#
#        # step code
#
#        return True # or False

# end
