# -*- coding:utf-8 -*-


from minimo import MoPerformer, \
    before_action, action_step, after_action


class BasePerformer(MoPerformer):
    """docstring for BasePerformer"""

    def __init__(self, name):
        super(BasePerformer, self).__init__(name)


# end
