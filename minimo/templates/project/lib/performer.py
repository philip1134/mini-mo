# -*- coding:utf-8 -*-


import minimo


class BasePerformer(minimo.Performer):
    """docstring for BasePerformer"""

    def __init__(self, name, logger=None, case_path=None):
        super(BasePerformer, self).__init__(
            name=name, logger=logger, case_path=case_path)


# end
