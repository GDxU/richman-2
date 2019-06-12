# -*- coding: utf-8 -*
'''房产类
'''
import logging

from richman.base import BasePlace, BasePlayer


class BuyPlaceWithOwnerException(Exception):
    def __init__(self, *args):
        super().__init__("该地已经卖出，无法购买！")

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

class SellPlaceWithNoOwner(Exception):
    def __init__(self, *args):
        super().__init__("该地无主，不能卖！")

class RebuyWithNoOwnerException(Exception):
    def __init__(self, *args):
        super().__init__("该地当前无主！")

class RebuyNotPledgedException(Exception):
    def __init__(self, *args):
        super().__init__("该地当前未被抵押！")


class PlaceImplement(BasePlace):

    __owner = None
    __is_pledged = False
    __buy_value = 0
    __pledge_value = 0

    def __init__(self, name: str, buy_value: int,
                 sell_value:int = None, pledge_value:int = None):
        '''init

        :param name: name of place
        :param buy_value: value to buy
        :param sell_value: value to sell, default is the buy_value
        :param pledge_value: value to pledge, can not be pledge if is None
        '''
        self.__name = name
        self.__buy_value = buy_value
        self.__sell_value = sell_value if sell_value else self.__buy_value
        self.__pledge_value = pledge_value
        # init others
        self.__owner = None
        self.__is_pledged = False
        # check
        assert pledge_value is None or self.sell_value >= pledge_value

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
    @property
    def sell_value(self):
        return self.__sell_value

    def buy(self, player: BasePlayer):
        if self.__owner:
            raise BuyPlaceWithOwnerException()
        else:
            player.add_money(-self.buy_value)
            self.__owner = player

    def pledge(self):
        if self.__owner is None:
            raise PledgeWithNoOwnerException()
        elif self.__is_pledged:
            raise PledgeTwiceException()
        else:
            self.owner.add_money(self.pledge_value)
            self.__is_pledged = True

    def sell(self):
        if not self.owner:
            raise SellPlaceWithNoOwner()
        sell_value = self.sell_value
        if self.is_pledged:
            sell_value -= self.pledge_value
        self.owner.add_money(sell_value)
        self.__owner = None

    def rebuy(self):
        if self.__owner is None:
            raise RebuyWithNoOwnerException()
        elif not self.__is_pledged:
            raise RebuyNotPledgedException()
        else:
            self.owner.add_money(-self.buy_value)
            self.__is_pledged = False

    def trigger(self, player: BasePlayer):
        '''take the effect of the place, triggered by the player
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        return self.name == obj.name


class PlaceEstate(PlaceImplement):

    __block = None
    __kMaxLevel = 4
    __current_level = 0

    def __init__(self, name: str, fees: list,
                 buy_value: int, pledge_value: int,
                 upgrade_value: int, block):
        '''init

        :param fees: fees accordding to estate level
        :param upgrade_value: money value to upgrade
        :param block: block that holds the place.
                      None if the place is a project.
        other params, refer to PlaceImplement
        '''
        super().__init__(name=name, buy_value=buy_value,
                         pledge_value=pledge_value)
        self.__fees = fees
        self.__upgrade_value = upgrade_value
        self.__block = block
        block.add_to_block(self)  # 将该地添加到对应 block
        # init others
        self.__kMaxLevel = 4
        self.__current_level = 0
        # check
        assert len(self.__fees) == self.__kMaxLevel
        assert fees == sorted(fees), \
            'fees of estate should go up with level up'

    @property
    def block(self):
        return self.__block
    @property
    def fee(self):
        return self.__fees[self.__current_level]
    @property
    def block_fee(self):
        return self.block.block_fee_calc(self.owner)
    @property
    def upgrade_value(self):
        return self.__upgrade_value

    def upgrade(self):
        if self.__current_level < self.__kMaxLevel:
            self.owner.add_money(-self.upgrade_value)
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

    def trigger(self, player: BasePlayer):
        '''if owner is not None, take the fee from player
        else ask player whether to buy the place
        '''
        # take the fee
        if self.owner and self.owner != player:
            self.owner.add_money(self.fee)
            player.add_money(-self.fee)
        # ask whether to buy
        else:
            player.trigger_buy(self)


class PlaceEstateBlock:
    '''a block that holds estates with same color
    '''

    __estates = []

    def __init__(self, name: str):
        '''init

        :param name: block name
        '''
        self.__name = name

    @property
    def name(self):
        return self.__name

    def add_to_block(self, estate: PlaceEstate):
        '''add estate to this block

        :param estate: estate to add
        '''
        assert isinstance(estate, PlaceEstate)
        self.__estates.append(estate)

    def block_fee_calc(self, owner: BasePlayer)->int:
        '''calculate block fee that belongs to the owner

        :param owner: the owner of the palces
        :return: the block fee
        '''
        block_fee = 0
        if owner is None:
            return block_fee
        for estate in self.__estates:
            if estate.owner and estate.owner == owner:
                block_fee += estate.fee
        return block_fee


class PlaceProject(PlaceImplement):
    def __init__(self, name, buy_value, sell_value):
        super().__init__(name=name, buy_value=buy_value,
                         pledge_value=0, sell_value=sell_value)


class PlaceProjectNuclear(PlaceProject):
    pass

class PlaceProjectBuilder(PlaceProject):
    pass

class PlaceProjectStation(PlaceProject):
    pass

class PlaceProjectTv(PlaceProject):
    pass

class PlaceProjectAirport(PlaceProject):
    pass

class PlaceProjectSewerage(PlaceProject):
    pass

class PlaceProjectSeaport(PlaceProject):
    pass

