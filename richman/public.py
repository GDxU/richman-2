# -*- coding: utf-8 -*
'''公用土地类，例如 新闻，公园 等无法买卖的公共地方
'''
import logging

import richman.interface as itf


class BasePublic:
    
    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name


class PublicStart(BasePublic):
    def __init__(self):
        super().__init__('起点')

class PublicNews(BasePublic):
    def __init__(self):
        super().__init__('新闻')

class PublicPrison(BasePublic):
    def __init__(self):
        super().__init__('监狱')

class PublicLuck(BasePublic):
    def __init__(self):
        super().__init__('运气')

class PublicStock(BasePublic):
    def __init__(self):
        super().__init__('证券中心')

class PublicGotoPrison(BasePublic):
    def __init__(self):
        super().__init__('入狱')

class PublicPark(BasePublic):
    def __init__(self):
        super().__init__('公园')

class PublicTax(BasePublic):
    def __init__(self):
        super().__init__('税务中心')