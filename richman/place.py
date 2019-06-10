# -*- coding: utf-8 -*
'''房产类
'''
import logging

from richman.player import (BasePlayer, PlayerMoneyBelowZeroException)


class BuyPlaceWithOwnerException(Exception):
    def __init__(self, *args):
        super().__init__("该地已经卖出，无法购买！")

class BuyPlaceWithoutEnoughMoneyException(Exception):
    def __init__(self, *args):
        super().__init__("玩家资金不够，无法购买！")

class UpgradeMaxException(Exception):
    def __init__(self, *args):
        super().__init__("已经满级，无法升级！")

class DegradeMinException(Exception):
    def __init__(self, *args):
        super().__init__("最低级，无法降级！")

class PledgeWithNoOwnerException(Exception):
    def __init__(self, *args):
        super().__init__("该地当前无主！")

class PledgeTwiceException(Exception):
    def __init__(self, *args):
        super().__init__("该地已经抵押！")

class RebuyWithNoOwnerException(Exception):
    def __init__(self, *args):
        super().__init__("该地当前无主！")

class RebuyNotPledgedException(Exception):
    def __init__(self, *args):
        super().__init__("该地当前未被抵押！")


class BasePlace:

    __owner = None
    __is_pledged = False
    __buy_value = 0
    __pledge_value = 0
    
    def __init__(self, name: str, buy_value: int,
                 pledge_value: int):
        '''init

        :param name: name of place
        :param buy_value: value to buy
        :param pledge_value: value to pledge
        '''
        self.__name = name
        self.__buy_value = buy_value
        self.__pledge_value = pledge_value
        # init others
        self.__owner = None
        self.__is_pledged = False

    @property
    def name(self):
        return self.__name
    @property
    def owner(self):
        return self.__owner
    @property
    def is_pledged(self):
        return self.__is_pledged
    @property
    def buy_value(self):
        return self.__buy_value
    @property
    def pledge_value(self):
        return self.__pledge_value

    def buy(self, owner: BasePlayer):
        if self.__owner:
            raise BuyPlaceWithOwnerException()
        elif owner.money < self.buy_value:
            raise BuyPlaceWithoutEnoughMoneyException()
        else:
            self.__owner = owner

    def pledge(self):
        if self.__owner is None:
            raise PledgeWithNoOwnerException()
        elif self.__is_pledged:
            raise PledgeTwiceException()
        else:
            self.__is_pledged = True

    def rebuy(self):
        if self.__owner is None:
            raise RebuyWithNoOwnerException()
        elif not self.__is_pledged:
            raise RebuyNotPledgedException()
        else:
            self.__is_pledged = False

    def take_effect(self, player: BasePlayer):
        '''take the effect of the place, triggered by the player
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        return self.name == obj.name


class PlaceEstate(BasePlace):

    __kMaxLevel = 3
    __current_level = 0

    def __init__(self, name: str, fees: list,
                 buy_value: int, pledge_value: int,
                 block):
        '''init

        :param fees: fees accordding to estate level
        :param block: block that holds the place.
                      None if the place is a project.
        other params, refer to BasePlace
        '''
        super().__init__(name=name, buy_value=buy_value,
                       pledge_value=pledge_value)
        self.__fees = fees
        self.block = block
        self.__kMaxLevel = 3
        self.__current_level = 0

    @property
    def block(self):
        return self.__block
    @block.setter
    def block(self, value):
        self.__block = value
    @property
    def fee(self):
        return self.__fees[self.__current_level]

    def upgrade(self):
        if self.__current_level < self.__kMaxLevel:
            self.__current_level += 1
            self.value = self.__fees[self.__current_level]
        else:
            raise UpgradeMaxException()

    def degrade(self):
        if self.__current_level > 0:
            self.__current_level -= 1
            self.value = self.__fees[self.__current_level]
        else:
            raise DegradeMinException()

    def take_effect(self, player: BasePlayer):
        '''if owner is not None, take the fee from player
        else ask player whether to buy the place
        '''
        # take the fee
        if self.owner and self.owner != player:
            self.owner.add_money(self.fee)
            try:
                player.add_money(-self.fee)
            except PlayerMoneyBelowZeroException as err:
                logging.info(str(err))
                player.no_money_action()
        # ask whether to buy
        else:
            player.buy_place_action(self)


class BlockEstate:
    '''a block that holds estates with same color
    '''

    def __init__(self, name: str, estates: list):
        '''init

        :param name: block name
        :param estates: list of estates belonging to block
        '''
        self.__estates = estates
        for estate in estates:
            self._add_to_block(estate)

    def _add_to_block(self, estate: PlaceEstate):
        estate.block = self


class PlaceProject(BasePlace):
    
    # def __init__(self, name: str, buy_value: int,
    #              pledge_value: int):
    #     super().__init__(name=name, buy_value=buy_value,
    #                    pledge_value=pledge_value)
    
    def take_effect(self, player: BasePlayer):
        pass