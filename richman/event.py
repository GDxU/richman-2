# -*- coding: utf-8 -*
'''事件类
'''
import logging

import richman.interface as itf


class EventImplement:
    
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class EventStart(EventImplement):
    def __init__(self):
        super().__init__('起点')

class EventNews(EventImplement):
    def __init__(self):
        super().__init__('新闻')

class EventPrison(EventImplement):
    def __init__(self):
        super().__init__('监狱')

class EventLuck(EventImplement):
    def __init__(self):
        super().__init__('运气')

class EventStock(EventImplement):
    def __init__(self):
        super().__init__('证券中心')

class EventGotoPrison(EventImplement):
    def __init__(self):
        super().__init__('入狱')

class EventPark(EventImplement):
    def __init__(self):
        super().__init__('公园')

class EventTax(EventImplement):
    def __init__(self):
        super().__init__('税务中心')