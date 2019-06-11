# -*- coding: utf-8 -*
'''player
'''
import random
import datetime


class PlayerMoneyBelowZeroException(Exception):
    def __init__(self, *args):
        super().__init__("玩家资金小于零！")


class BasePlayer:

    __places = []  # 购买的土地
    __pos = 0  # 当前所在地图的位置
    __pos_max = 0  # 地图最大 pos 值

    def __init__(self, name: str, money: int):
        '''init

        :param name: player name
        :param money: player's init money
        '''
        self.__name = name
        self.money = money
        # init others
        self.__places = []
        self.__pos = 0
        random.seed(datetime.datetime.now())

    @property
    def name(self):
        return self.__name
    @property
    def money(self):
        return self.__money
    @money.setter
    def money(self, value):
        if value < 0:
            raise PlayerMoneyBelowZeroException()
        else:
            self.__money = value
    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, value: int):
        self.__pos = value % self.pos_max
    @property
    def pos_max(self):
        return self.__pos_max
    @pos_max.setter
    def pos_max(self, value: int):
        assert value > 0, 'mas pos of map should be bigger than zero.'
        self.__pos_max = value
    @property
    def places(self):
        return self.__places

    def add_money(self, value: int):
        self.money += value

    def buy_place_action(self, place):
        '''决策是否购买该地

        :param place: BasePlace
        '''
        place.buy(self)
        self.__places.append(place)

    def no_money_action(self):
        '''没有钱的时候进行决策
        '''
        pass

    def _dice(self)->int:
        return random.randrange(1,7)

    def play(self):
        '''进行下一步游戏
        '''
        self.pos += self._dice()

    def __eq__(self, obj):
        return self.name == obj.name
