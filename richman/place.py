# -*- coding: utf-8 -*
'''房产类
'''
import typing
import logging

import richman.interface as itf
import richman.event as ev


# base place

class BasePlace(itf.IPlayerForPlace, itf.IMapForPlace):

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
        self.__owner:itf.IPlaceForPlayer = None

    @property
    def buy_value(self)->int:
        return self.__buy_value
    @property
    def sell_value(self)->int:
        return self.__sell_value
    @property
    def is_available(self)->bool:
        return self.owner is None
    @property
    def name(self)->str:
        return self.__name
    @property
    def owner(self)->itf.IPlaceForPlayer:
        return self.__owner

    def _exchange_money(self,
                        player_src: itf.IPlaceForPlayer,
                        player_dst: itf.IPlaceForPlayer,
                        money_delta: int):
        '''take money_delta from src to dst player

        :param player_src: src of player to subtract money_delta
        :param player_dst: dst of player to add money_delta
        :param money_delta: amount of money_delta to take
        '''
        assert money_delta > 0, '交换费用需要大于零！'
        ev.event_to_player_add_money.send(self, receiver=player_src,
                                          money_delta=-money_delta)
        ev.event_to_player_add_money.send(self, receiver=player_dst,
                                          money_delta=money_delta)

    @staticmethod
    @ev.event_to_place_buy.connect
    def event_handler_buy(sender: itf.IPlaceForPlayer, **kwargs):
        '''set the owner to the buyer

        :param sender: player to buy the place
        :param kwargs: holds receiver of place to buy
        '''
        self:BasePlace = kwargs['receiver']
        buyer = sender
        assert self.__owner is None, '该地已经卖出，无法购买！'
        self.__owner = buyer
        logging.info('{} 购买地产（项目） {}，花费 {} 元。'.format(buyer.name, self.name, self.buy_value))

    @staticmethod
    @ev.event_to_place_sell.connect
    def event_handler_sell(sender: itf.IPlaceForPlayer, **kwargs):
        '''remove the owner

        :param sender: player to sell the place
        :param kwargs: holds receiver of place to sell
        '''
        self:BasePlace = kwargs['receiver']
        seller = sender
        assert seller == self.owner, '该地产（项目）不归 {} 所有，无法变卖！'.format(seller.name)
        assert self.owner is not None, '该地无主，不能卖！'
        logging.info('{} 变卖地产（项目） {}，获得 {} 元。'.format(self.owner.name, self.name, self.sell_value))
        self.__owner = None
        self.reset()

    def trigger(self, player: itf.IPlaceForPlayer):
        raise NotImplementedError('need override')

    def reset(self):
        raise NotImplementedError('need override')

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display place info
        '''
        raise NotImplementedError('need override')


# estate

class Estate(BasePlace, itf.IMapForEstate, itf.IPlayerForEstate):

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
        super().__init__(name, buy_value, sell_value=buy_value)
        self.__fees = fees
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
    def upgrade_value(self)->int:
        return self.__upgrade_value
    @property
    def sell_value(self)->int:
        if self.is_pledged:
            return self.buy_value - self.pledge_value
        return self.buy_value
    @property
    def is_pledged(self)->bool:
        return self.__is_pledged
    @property
    def pledge_value(self)->int:
        return self.__pledge_value
    @property
    def is_level_max(self)->int:
        return self.current_level >= (self.__kMaxLevel - 1)
    @property
    def current_level(self)->int:
        return self.__current_level
    @property
    def block(self):
        return self.__block
    @property
    def fee(self)->int:
        return self.__fees[self.current_level]
    @property
    def fees(self)->int:
        return self.__fees

    @staticmethod
    @ev.event_to_estate_upgrade.connect
    def event_handler_upgrade(sender: itf.IEstateForPlayer, **kwargs):
        '''upgrade estate

        :param sender: player to upgrade
        :param kwargs: holds receiver of estate
        '''
        self:Estate = kwargs['receiver']
        player = sender
        if player is None:
            print('player is none.')
        if self.owner is None:
            print('owner is none.')
            print(self)
        assert player == self.owner, '该地产不归 {} 所有，无法升级！'.format(player.name)
        assert not self.is_level_max, '已经满级，无法升级！'
        self.__current_level += 1
        logging.info('{} 升级地产 {} 到 {} 级，花费 {} 元。'.format(self.owner.name,
                                                                  self.name,
                                                                  self.current_level,
                                                                  self.upgrade_value))

    @staticmethod
    @ev.event_to_estate_degrade.connect
    def event_handler_degrade(sender: itf.IEstateForPlayer, **kwargs):
        '''degrade estate

        :param sender: player to degrade
        :param kwargs: holds receiver of estate
        '''
        self:Estate = kwargs['receiver']
        player = sender
        assert player == self.owner, '该地产不归 {} 所有，无法降级！'.format(player.name)
        assert self.current_level > 0, '最低级，无法降级！'
        self.__current_level -= 1
        logging.info('{} 降低地产 {} 等级到 {} 级。'.format(self.owner.name, self.name, self.current_level))

    @staticmethod
    @ev.event_to_estate_pledge.connect
    def event_handler_pledge(sender: itf.IEstateForPlayer, **kwargs):
        '''pledge the estate

        :param sender: player to pledge
        :param kwargs: holds receiver of estate
        '''
        self:Estate = kwargs['receiver']
        player = sender
        assert player == self.owner, '该地产不归 {} 所有，无法抵押！'.format(player.name)
        assert self.owner is not None, '该地当前无主，无法抵押！'
        assert not self.is_pledged, '该地已经抵押！'
        self.__is_pledged = True
        logging.info('{} 抵押地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.pledge_value))

    @staticmethod
    @ev.event_to_estate_rebuy.connect
    def event_handler_rebuy(sender: itf.IEstateForPlayer, **kwargs):
        '''pledge the estate

        :param sender: player to rebuy
        :param kwargs: holds receiver of estate
        '''
        self:Estate = kwargs['receiver']
        player = sender
        assert player == self.owner, '该地产不归 {} 所有，无法赎回！'.format(player.name)
        assert self.owner is not None, '该地当前无主，赎回无效！'
        assert self.is_pledged, '该地当前未被抵押！'
        self.__is_pledged = False
        logging.info('{} 赎回地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.buy_value))

    def trigger(self, player: itf.IEstateForPlayer):
        '''override if owner is not None, take the fee from player
        else ask player whether to buy the place
        '''
        logging.info('{} 走到 {}。'.format(player.name, self.name))
        # has owner
        if self.owner:
            # take the fee
            if self.owner != player:
                block_fee = self.block.block_fee_calc(self.owner)
                logging.info('{} 交给 {} 地租 {}。'.format(player.name, self.owner.name, block_fee))
                self._exchange_money(player, self.owner, block_fee)
            # upgrade
            else:
                ev.event_to_player_upgrade_estate.send(self, receiver=player)
        # ask whether to buy
        else:
            ev.event_to_player_buy_place.send(self, receiver=player)

    def reset(self):
        self.__current_level = 0

    def __str__(self):
        '''override display place info
        '''
        lines = '{}: {}, {}, {}'.format(self.name,
                                        self.owner.name,
                                        self.current_level,
                                        'x' if self.is_pledged else 'o')
        return lines


class EstateBlock:
    '''a block that holds estates with same color
    '''

    def __init__(self, name: str):
        '''init

        :param name: block name
        '''
        self.__name = name
        self.__estates:typing.List[Estate] = []

    @property
    def name(self)->str:
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


# project

class Project(BasePlace, itf.IPlayerForProject, itf.IMapForProject):

    def trigger(self, player: itf.IProjectForPlayer):
        '''override take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        if self.owner:
            self._take_effect(player)
        else:
            ev.event_to_player_buy_place.send(self, receiver=player)

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        raise NotImplementedError('override is needed.')

    def reset(self):
        pass

    def __eq__(self, obj):
        '''override project is always not equal
        '''
        return False

    def __str__(self):
        '''override display project info
        '''
        return '{}: {}'.format(self.name, self.owner.name)


class ProjectNuclear(Project):

    def __init__(self):
        '''init
        '''
        super().__init__(name='核能发电站',
                         buy_value=3500,
                         sell_value=3000)

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''收取500元，若对方拥有1级/2级/3级地产，额外收取500/1000/1500元。

        :param player: IProjectForPlayer
        '''
        fine = 500 + 500 * player.estate_max_level
        logging.info('{} 走到 {}，缴付 {} 元。'.format(player.name, self.name, fine))
        self._exchange_money(player, self.owner, fine)


class ProjectBuilder(Project):

    def __init__(self):
        '''init
        '''
        super().__init__(name='建筑公司',
                         buy_value=4000,
                         sell_value=3000)

    # def buy(self, player: itf.IProjectForPlayer):
    #     '''override
    #     '''
    #     super().buy(player)
    #     # 注册 upgrade callback
    #     import richman.estate as est
    #     est.BaseEstate.add_to_static_callbacks_upgrade(self.__someone_upgraded_estate)

    # def sell(self):
    #     '''override
    #     '''
    #     super().sell()
    #     # 注销 upgrade callback
    #     import richman.estate as est
    #     est.BaseEstate.remove_from_static_callbacks_upgrade(self.__someone_upgraded_estate)

    # def __someone_upgraded_estate(self, estate: itf.IProjectForEstate,
    #                               player: itf.IProjectForPlayer):
    #     '''有人升级房屋，该人需要支付 500 元给 owner of builder
    #     '''
    #     if not player:
    #         print('player is None!!!!!!!!!')
    #     if not self.owner:
    #         print('owner is None!!!!!!!!!')
    #     if player == self.owner:
    #         return None
    #     fine = 500
    #     logging.info('{} 升级地产，需向 {} 支付 {} 元升级费。'.format(player.name,
    #                                                                self.owner.name,
    #                                                                fine))
    #     player.add_money(-fine)

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''每当玩家升级地产时，获得500元。
        当任意玩家到建筑公司时，可将一处地产升一级（需支付升级费用）。

        :param player: IProjectForPlayer
        '''
        logging.info('{} 走到 {}，可选择一处地产升级。'.format(player.name, self.name))
        ev.event_to_player_upgrade_any_estate.send(self, receiver=player)
