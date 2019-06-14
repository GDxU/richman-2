# -*- coding: utf-8 -*
'''房产类
'''
import logging

import richman.interface as itf


class BaseEstate(itf.IPlayerForEstate, itf.IMapForEstate):

    def __init__(self, name: str, fees: list,
                 buy_value: int, pledge_value: int,
                 upgrade_value: int, block):
        '''init

        :param name: name of place
        :param fees: fees accordding to estate level
        :param buy_value: value to buy
        :param pledge_value: value to pledge, can not be pledge if is None
        :param upgrade_value: money value to upgrade
        :param block: block that holds the place.
        '''
        self.__name = name
        self.__fees = fees
        self.__buy_value = buy_value
        self.__pledge_value = pledge_value
        self.__upgrade_value = upgrade_value
        self.__block = block
        block.add_to_block(self)  # 将该地添加到对应 block
        # init others
        self.__owner = None
        self.__is_pledged = False
        self.__kMaxLevel = 4
        self.__current_level = 0
        # check
        assert len(self.__fees) == self.__kMaxLevel
        assert fees == sorted(fees), \
            'fees of estate should go up with level up'
        assert self.sell_value > self.pledge_value


    @property
    def buy_value(self):
        return self.__buy_value
    @property
    def upgrade_value(self):
        return self.__upgrade_value
    @property
    def sell_value(self):
        if self.is_pledged:
            return self.__buy_value - self.pledge_value
        return self.__buy_value
    @property
    def is_pledged(self):
        return self.__is_pledged
    @property
    def pledge_value(self):
        return self.__pledge_value
    @property
    def is_available(self):
        return self.owner is None
    @property
    def is_level_max(self):
        return self.current_level >= (self.__kMaxLevel - 1)
    @property
    def current_level(self):
        return self.__current_level

    @property
    def name(self):
        return self.__name
    @property
    def owner(self):
        return self.__owner
    @property
    def block(self):
        return self.__block
    @property
    def fee(self):
        return self.__fees[self.__current_level]

    def buy(self, player: itf.IEstateForPlayer):
        assert self.__owner is None, '该地已经卖出，无法购买！'
        player.add_money(-self.buy_value)
        self.__owner = player
        logging.info('{} 购买地产 {}，花费 {} 元。'.format(player.name, self.name, self.buy_value))

    def upgrade(self):
        assert not self.is_level_max, '已经满级，无法升级！'
        self.owner.add_money(-self.upgrade_value)
        self.__current_level += 1
        self.value = self.__fees[self.__current_level]
        logging.info('{} 升级地产 {} 到 {} 级，花费 {} 元。'.format(self.owner.name,
                                                                  self.name,
                                                                  self.__current_level,
                                                                  self.upgrade_value))

    def degrade(self):
        assert self.current_level > 0, '最低级，无法降级！'
        self.__current_level -= 1
        self.value = self.__fees[self.__current_level]
        logging.info('{} 降低地产 {} 等级到 {} 级。'.format(self.owner.name, self.name, self.__current_level))

    def sell(self):
        assert self.owner is not None, '该地无主，不能卖！'
        self.owner.add_money(self.sell_value)
        logging.info('{} 变卖地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.sell_value))
        self.__owner = None
        self.__current_level = 0

    def pledge(self):
        assert self.owner is not None, '该地当前无主，无法抵押！'
        assert not self.is_pledged, '该地已经抵押！'
        self.owner.add_money(self.pledge_value)
        self.__is_pledged = True
        logging.info('{} 抵押地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.pledge_value))

    def rebuy(self):
        assert self.owner is not None, '该地当前无主，赎回无效！'
        assert self.is_pledged, '该地当前未被抵押！'
        self.owner.add_money(-self.buy_value)
        self.__is_pledged = False
        logging.info('{} 赎回地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.buy_value))

    def trigger(self, player: itf.IEstateForPlayer):
        '''if owner is not None, take the fee from player
        else ask player whether to buy the place
        '''
        logging.info('{} 走到 {}。'.format(player.name, self.name))
        # has owner
        if self.owner:
            # take the fee
            if self.owner != player:
                block_fee = self.block.block_fee_calc(self.owner)
                logging.info('{} 交给 {} 地租 {}。'.format(player.name, self.owner.name, block_fee))
                self.owner.add_money(block_fee)
                player.add_money(-block_fee)
            # update
            else:
                player.trigger_upgrade(self)
        # ask whether to buy
        else:
            player.trigger_buy(self)

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display place info
        '''
        lines = '{}: {}'.format(self.name, self.__current_level)
        return lines


class Estate(BaseEstate):
    pass


class EstateBlock:
    '''a block that holds estates with same color
    '''

    def __init__(self, name: str):
        '''init

        :param name: block name
        '''
        self.__name = name
        self.__estates = []

    @property
    def name(self):
        return self.__name

    def add_to_block(self, estate: Estate):
        '''add estate to this block

        :param estate: estate to add
        '''
        assert isinstance(estate, Estate)
        self.__estates.append(estate)

    def block_fee_calc(self, owner: itf.IEstateForPlayer)->int:
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

