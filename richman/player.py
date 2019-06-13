# -*- coding: utf-8 -*
'''player
'''
import random
import datetime

import richman.interface as itf


class PlayerBanckruptException(Exception):
    def __init__(self, *args):
        super().__init__("玩家破产！")


class PlayerImplement(itf.IGamePlayer, itf.IMapPlayer,
                      itf.IPlacePlayer):

    __name = ''
    __money = 0
    __map = None
    __places = []  # 购买的土地
    __pos = 0  # 当前所在地图的位置

    def __init__(self, name: str, money: int,
                 map:itf.IPlayerMap = None):
        '''init

        :param name: player name
        :param money: player's init money
        '''
        self.__name = name
        assert money > 0, '初始资金必须大于零。'
        self.__money = money
        self.__map = map
        # init others
        self.__places = []
        self.__pos = 0
        random.seed(datetime.datetime.now())

    @property
    def name(self):
        return self.__name
    @property
    def is_banckrupted(self):
        raise NotImplementedError('need override.')
    @property
    def money(self):
        return self.__money
    @property
    def map(self):
        return self.__map
    @map.setter
    def map(self, value: itf.IPlayerMap):
        self.__map = value
    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, value: int):
        self.__pos = value % len(self.__map)
    @property
    def places(self):
        return self.__places

    def _dice(self)->int:
        return random.randrange(1,7)

    def add_to_map(self, map: itf.IPlayerMap):
        '''add player to map

        :param map: map
        '''
        self.__map = map

    __is_making_money = False  # 防止一个 make_money() 过程中多次调用该函数
    def add_money(self, delta: int):
        '''change the player's money

        :param delta: amount of change, minus means subtraction
        '''
        self.__money += delta
        if self.__money < 0 and not self.__is_making_money:
            self.__is_making_money = True
            self._make_money()
            self.__is_making_money = False

    def move_to(self, pos: int):
        '''move player to pos

        :param pos: position to move to
        '''
        self.pos = pos

    def play(self, reverse=False):
        '''进行下一步游戏

        :param reverse: 是否后退标志
        '''
        step = self._dice()
        if reverse:
            step = 0 - step
        self.pos += step

    def trigger_buy(self, place: itf.IPlayerPlace):
        '''decide whether to buy the place

        :param place: IPlayerPlace
        '''
        if self._trigger_buy(place):
            self.__places.append(place)

    def trigger_jump_to_estate(self):
        '''select which estate to go when jump is needed
        '''
        self._trigger_jump_to_estate()

    def _make_money(self):
        '''make money my pledging or selling,
        to make player's money more than zero
        '''
        raise NotImplementedError('override is needed.')

    def _trigger_buy(self, place: itf.IPlayerPlace)->bool:
        '''decide whether to buy the place

        :param place: BasePlace
        :return: True if buy the place
        '''
        raise NotImplementedError('override is needed.')

    def _trigger_jump_to_estate(self):
        '''select which estate to go when jump is needed
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        return self.name == obj.name


class PlayerSimple(PlayerImplement):

    @property
    def is_banckrupted(self):
        raise NotImplementedError('need override.')

    def _make_money(self):
        '''make money my pledging or selling,
        to make player's money more than zero
        '''
        # pledge for money
        for place in self.places:
            if place.pledge_value is not None:
                place.pledge()
                if self.money > 0:
                    return None
        # sell for money
        for place in self.places:
            place.sell()
            if self.money > 0:
                return None
        # banckrupt
        raise PlayerBanckruptException()

    def _trigger_buy(self, place: itf.IPlayerPlace)->bool:
        '''decide whether to buy the place

        :param place: BasePlace
        :return: True if buy the place
        '''
        if self.money > place.buy_value:
            place.buy(self)
            return True
        else:
            return False

    def _trigger_jump_to_estate(self):
        '''select which estate to go when jump is needed
        '''
        for index, item in enumerate(self.map.items):
            if (isinstance(item, itf.IPlayerPlace)
                    and item.pledge_value is not None):
                self.pos = index
                break


class PlayerPerson(PlayerImplement):
    pass


class PlayerCpu(PlayerImplement):
    pass