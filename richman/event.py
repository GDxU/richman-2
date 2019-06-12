# -*- coding: utf-8 -*
'''事件类
'''
import logging

from richman.player import (BasePlayer, PlayerMoneyBelowZeroException)


class BaseEvent:
    
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def trigger(self, player: BasePlayer):
        '''take the effect of the place, triggered by the player
        '''
        raise NotImplementedError('override is needed.')

class EventStart(BaseEvent):
    def __init__(self):
        super().__init__('起点')

class EventNews(BaseEvent):
    def __init__(self):
        super().__init__('新闻')

class EventPrison(BaseEvent):
    def __init__(self):
        super().__init__('监狱')

class EventLuck(BaseEvent):
    def __init__(self):
        super().__init__('运气')

class EventStock(BaseEvent):
    def __init__(self):
        super().__init__('证券中心')

class EventGotoPrison(BaseEvent):
    def __init__(self):
        super().__init__('入狱')

class EventPark(BaseEvent):
    def __init__(self):
        super().__init__('公园')

class EventTax(BaseEvent):
    def __init__(self):
        super().__init__('税务中心')