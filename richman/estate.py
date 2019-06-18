# -*- coding: utf-8 -*
'''房产类
'''
import logging

import richman.interface as itf
import richman.event as ev


class BaseEstate(itf.IPlayerForEstate, itf.IMapForEstate):

    def __init__(self, event_manager: itf.IForEventManager,
                 name: str, fees: list,
                 buy_value: int, pledge_value: int,
                 upgrade_value: int, block):
        '''init

        :param event_manager: event manager interface
        :param name: name of place
        :param fees: fees accordding to estate level
        :param buy_value: value to buy
        :param pledge_value: value to pledge, can not be pledge if is None
        :param upgrade_value: money value to upgrade
        :param block: block that holds the place.
        '''
        self.__event_manager = event_manager
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
    @property
    def fees(self):
        return self.__fees

    def event_handler_buy(self, event: ev.EventToPlaceBuy):
        '''set the owner to the buyer

        :param event: EventToPlaceBuy with buyer
        '''
        assert self.__owner is None, '该地已经卖出，无法购买！'
        buyer = event.player
        self.__owner = buyer
        logging.info('{} 购买地产 {}，花费 {} 元。'.format(buyer.name, self.name, self.buy_value))

    def event_handler_upgrade(self, event: ev.EventToEstateUpgrade):
        '''upgrade estate

        :param event: EventToEstateUpgrade with player
        '''
        assert event.player == self.owner, '该地产不归 {} 所有，无法升级！'.format(event.player.name)
        assert not self.is_level_max, '已经满级，无法升级！'
        self.__current_level += 1
        logging.info('{} 升级地产 {} 到 {} 级，花费 {} 元。'.format(self.owner.name,
                                                                  self.name,
                                                                  self.__current_level,
                                                                  self.upgrade_value))

    def event_handler_degrade(self, event: ev.EventToEstateDegrade):
        '''degrade estate

        :param event: EventToEstateDegrade with player
        '''
        assert event.player == self.owner, '该地产不归 {} 所有，无法降级！'.format(event.player.name)
        assert self.current_level > 0, '最低级，无法降级！'
        self.__current_level -= 1
        logging.info('{} 降低地产 {} 等级到 {} 级。'.format(self.owner.name, self.name, self.__current_level))

    def event_handler_sell(self, event: ev.EventToPlaceSell):
        '''remove the owner

        :param event: EventToPlaceSell with seller
        '''
        assert event.player == self.owner, '该地产不归 {} 所有，无法变卖！'.format(event.player.name)
        assert self.owner is not None, '该地无主，不能卖！'
        logging.info('{} 变卖地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.sell_value))
        self.__owner = None
        self.__current_level = 0

    def event_handler_pledge(self, event: ev.EventToEstatePledge):
        '''pledge the estate

        :param event: EventToEstatePledge with owner
        '''
        assert event.player == self.owner, '该地产不归 {} 所有，无法抵押！'.format(event.player.name)
        assert self.owner is not None, '该地当前无主，无法抵押！'
        assert not self.is_pledged, '该地已经抵押！'
        self.__is_pledged = True
        logging.info('{} 抵押地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.pledge_value))

    def event_handler_rebuy(self, event: ev.EventToEstateRebuy):
        '''pledge the estate

        :param event: EventToEstatePledge with owner
        '''
        assert event.player == self.owner, '该地产不归 {} 所有，无法赎回！'.format(event.player.name)
        assert self.owner is not None, '该地当前无主，赎回无效！'
        assert self.is_pledged, '该地当前未被抵押！'
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
                self.__event_manager.send(ev.EventToPlayerAddMoney(self.owner.name, block_fee))
                self.__event_manager.send(ev.EventToPlayerAddMoney(player.name, -block_fee))
            # update
            else:
                self.__event_manager.send(ev.EventToPlayerUpgradeEstate(player.name, self))
        # ask whether to buy
        else:
            self.__event_manager.send(ev.EventToPlayerBuyPlace(player.name, self))

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display place info
        '''
        lines = '{}: {}, {}'.format(self.name, self.__current_level,
                                    'x' if self.is_pledged else 'o')
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

