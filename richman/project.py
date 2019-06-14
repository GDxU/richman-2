# -*- coding: utf-8 -*
'''项目类
'''
import logging

import richman.interface as itf


class BaseProject(itf.IPlayerForProject):

    def __init__(self, name: str, buy_value: int, sell_value: int):
        '''init

        :param name: name of place
        :param buy_value: value to buy
        :param sell_value: value to sell
        '''
        self.__name = name
        self.__buy_value = buy_value
        self.__sell_value = sell_value
        # init others
        self.__owner = None

    @property
    def name(self):
        return self.__name
    @property
    def owner(self):
        return self.__owner
    @property
    def buy_value(self):
        return self.__buy_value
    @property
    def sell_value(self):
        return self.__sell_value

    def buy(self, player: itf.IPlaceForPlayer):
        assert not self.__owner, '该项目已经卖出，无法购买！'
        player.add_money(-self.buy_value)
        self.__owner = player
        logging.info('{} 购买项目 {}，花费 {} 元。'.format(player.name, self.name, self.buy_value))

    def sell(self):
        assert self.owner, '该项目无主，不能卖！'
        self.owner.add_money(self.sell_value)
        logging.info('{} 变卖项目 {}，获得 {} 元。'.format(self.owner.name, self.name, self.sell_value))
        self.__owner = None

    def trigger(self, player: itf.IProjectForPlayer):
        '''take the effect of the place, triggered by the player
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display project info
        '''
        return self.name


class PlaceProjectNuclear(BaseProject):
    pass

class PlaceProjectBuilder(BaseProject):
    pass

class PlaceProjectStation(BaseProject):
    pass

class PlaceProjectTv(BaseProject):
    pass

class PlaceProjectAirport(BaseProject):
    pass

class PlaceProjectSewerage(BaseProject):
    pass

class PlaceProjectSeaport(BaseProject):
    pass

