# -*- coding:utf-8 -*-
#
# author: philip1134
# date: 2017-08-08
#

import time

class Timer(object):
    """计时器，初始化时即开始计时"""
    
    timers = {}
    
    def __init__(self, name):
        self.started_at = time.time()
        self.name = name
        
        Timer.timers[name] = self

    def duration(self):
        """计算起始到当前所经历的时间，单位'秒'"""
        return time.time() - self.started_at
    
    @classmethod
    def get(cls, name):
        """获取指定 {name} 的计时器"""
        return cls.timers[name]
# end