# -*- coding: utf-8 -*
'''房产类
'''
import math
from typing import Any, List, Tuple, Optional, cast
import logging

import richman.interface as itf
import richman.event as ev


# base place

class BasePlace(itf.IPlayerForPlace, itf.IMapForPlace, itf.IPublicForPlace):

    def __init__(self, name: str, buy_value: int, sell_value: int,
                 pos_in_map: int)->None:
        '''init

        :param name: name of place
        :param buy_value: value to buy
        :param sell_value: value to sell
        :param pos_in_map: position in map
        '''
        self.__name = name
        self.__buy_value = buy_value
        self.__sell_value = sell_value
        self.__pos_in_map: int = pos_in_map
        # init others
        self.__owner:Optional[itf.IPlaceForPlayer] = None

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
    def owner(self)->Optional[itf.IPlaceForPlayer]:
        return self.__owner
    @property
    def pos_in_map(self)->int:
        return self.__pos_in_map
    
    def _subtract_money(self, player: itf.IPlaceForPlayer,
                        amount: int)->bool:
        '''subtract player's money and check if succeeds

        :param player: player to subtract from
        :param amount: money to subtract
        :return: True if succeeds
        '''
        assert amount > 0
        results:List[Tuple[Any, Optional[bool]]] =\
            ev.event_to_player_add_money.send(self, player=player, money_delta=-amount)
        return ev.check_event_result_is_true(results)

    def _add_money(self, player: itf.IPlaceForPlayer, amount: int)->None:
        '''add player's money and check if succeeds

        :param player: player to subtract from
        :param amount: money to subtract
        '''
        assert amount > 0
        ev.event_to_player_add_money.send(self, player=player, money_delta=amount)

    def _exchange_money(self,
                        player_src: itf.IPlaceForPlayer,
                        player_dst: itf.IPlaceForPlayer,
                        money_delta: int)->bool:
        '''take money_delta from src to dst player

        :param player_src: src of player to subtract money_delta
        :param player_dst: dst of player to add money_delta
        :param money_delta: amount of money_delta to take
        :return: True if succeeds
        '''
        rst = self._subtract_money(player=player_src,
                                   amount=money_delta)
        if not rst:
            logging.warning('扣钱失败，当前玩家 {} 余额： {} 。'.format(player_src.name, player_src.money))
            return False
        self._add_money(player=player_dst,
                        amount=money_delta)
        return True

    def _buy(self, buyer: itf.IPlaceForPlayer)->None:
        '''set the owner to the buyer

        :param buyer: buyer to buy the place
        '''
        assert self.__owner is None, '该地已经卖出，无法购买！'
        rst = self._subtract_money(buyer, self.buy_value)
        if not rst:
            logging.warning('购买失败，当前玩家 {} 余额 {}。'.format(buyer.name, buyer.money))
            return None
        self.__owner = buyer
        logging.info('{} 购买地产（项目） {}，花费 {} 元。'.format(buyer.name, self.name, self.buy_value))

    def _sell(self, seller: itf.IPlaceForPlayer)->None:
        '''remove the owner

        :param seller: seller to sell place
        '''
        assert seller == self.owner, '该地产（项目）不归 {} 所有，无法变卖！'.format(seller.name)
        assert self.owner is not None, '该地无主，不能卖！'
        self._add_money(seller, self.sell_value)
        logging.info('{} 变卖地产（项目） {}，获得 {} 元。'.format(self.owner.name, self.name, self.sell_value))
        self.__owner = None

    @staticmethod
    @ev.event_to_place_buy.connect
    def event_handler_buy(sender: itf.IPlaceForPlayer,
                          place)->None:
        '''set the owner to the buyer

        :param sender: player to buy the place
        :param place: place to buy
        '''
        self:BasePlace = place
        buyer = sender
        self._buy(buyer)

    @staticmethod
    @ev.event_to_place_sell.connect
    def event_handler_sell(sender: itf.IPlaceForPlayer,
                           place)->None:
        '''remove the owner

        :param sender: player to sell the place
        :param place: place to sell
        '''
        self:BasePlace = place
        seller = sender
        self._sell(seller)

    def trigger(self, player: Any)->None:
        raise NotImplementedError('need override')

    def destroy(self)->None:
        '''destroy
        '''
        pass

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
                 upgrade_value: int, block, pos_in_map: int):
        '''init

        :param name: name of place
        :param fees: fees accordding to estate level
        :param buy_value: value to buy
        :param pledge_value: value to pledge, can not be pledge if is None
        :param upgrade_value: money value to upgrade
        :param block: block that holds the place.
        :param pos_in_map: position in map
        '''
        super().__init__(name, buy_value, sell_value=buy_value, pos_in_map=pos_in_map)
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
            'fees of %s should go up with level up' % name
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
        if self.is_pledged:
            return 0
        else:
            return self.__fees[self.current_level]
    @property
    def fees(self)->List[int]:
        return self.__fees
    @property
    def block_fee(self)->int:
        if self.is_pledged:
            return 0
        else:
            return self.block.block_fee_calc(self.owner)

    def _buy(self, buyer: itf.IPlaceForPlayer)->None:
        '''override, set the owner to the buyer

        :param buyer: buyer to buy the place
        '''
        super()._buy(buyer)
        ev.event_from_estate_bought.send(self)

    def _sell(self, seller: itf.IPlaceForPlayer)->None:
        '''override, override, remove the owner

        :param seller: seller to sell place
        '''
        super()._sell(seller)
        self.__current_level = 0
        self.__is_pledged = False
        ev.event_from_estate_sold.send(self)

    def _upgrade(self, player: itf.IEstateForPlayer)->None:
        '''upgrade estate

        :param player: player to upgrade
        '''
        assert self.owner is not None
        assert player == self.owner, '该地产不归 {} 所有，无法升级！'.format(player.name)
        assert not self.is_level_max, '已经满级，无法升级！'
        rst = self._subtract_money(player, self.upgrade_value)
        if not rst:
            logging.warning('升级失败，当前玩家 {} 余额 {}。'.format(player.name, player.money))
        self.__current_level += 1
        ev.event_from_estate_upgraded.send(self)
        logging.info('{} 升级地产 {} 到 {} 级，花费 {} 元。'.format(self.owner.name,
                                                                  self.name,
                                                                  self.current_level,
                                                                  self.upgrade_value))

    def _degrade(self, player: itf.IEstateForPlayer)->None:
        '''degrade estate

        :param player: player to degrade
        '''
        assert self.owner is not None
        assert player == self.owner, '该地产不归 {} 所有，无法降级！'.format(player.name)
        assert self.current_level > 0, '最低级，无法降级！'
        self.__current_level -= 1
        ev.event_from_estate_degraded.send(self)
        logging.info('{} 降低地产 {} 等级到 {} 级。'.format(self.owner.name, self.name, self.current_level))

    def _pledge(self, player: itf.IEstateForPlayer)->None:
        '''pledge the estate

        :param player: player to pledge
        '''
        assert self.owner is not None, '该地当前无主，无法抵押！'
        assert player == self.owner, '该地产不归 {} 所有，无法抵押！'.format(player.name)
        assert not self.is_pledged, '该地已经抵押！'
        self._add_money(player, self.pledge_value)
        self.__is_pledged = True
        ev.event_from_estate_pledged.send(self)
        logging.info('{} 抵押地产 {}，获得 {} 元。'.format(self.owner.name, self.name, self.pledge_value))

    def _rebuy(self, player: itf.IEstateForPlayer)->None:
        '''rebuy pledged estate

        :param player: player to rebuy
        '''
        assert self.owner is not None, '该地当前无主，赎回无效！'
        assert player == self.owner, '该地产不归 {} 所有，无法赎回！'.format(player.name)
        assert self.is_pledged, '该地当前未被抵押！'
        rst = self._subtract_money(player, self.buy_value)
        if not rst:
            logging.warning('赎回地产失败，当前玩家 {} 余额 {}。'.format(player.name, player.money))
            return None
        self.__is_pledged = False
        ev.event_from_estate_rebought.send(self)
        logging.info('{} 赎回地产 {}，花费 {} 元。'.format(self.owner.name, self.name, self.buy_value))

    @staticmethod
    @ev.event_to_estate_upgrade.connect
    def event_handler_upgrade(sender: itf.IEstateForPlayer, estate)->None:
        '''upgrade estate

        :param sender: player to upgrade
        :param estate: estate to upgrade
        '''
        self:Estate = estate
        player = sender
        self._upgrade(player)

    @staticmethod
    @ev.event_to_estate_degrade.connect
    def event_handler_degrade(sender: itf.IEstateForPlayer, estate):
        '''degrade estate

        :param sender: player to degrade
        :param estate: estate to degrade
        '''
        self:Estate = estate
        player = sender
        self._degrade(player)

    @staticmethod
    @ev.event_to_estate_pledge.connect
    def event_handler_pledge(sender: itf.IEstateForPlayer, estate):
        '''pledge the estate

        :param sender: player to pledge
        :param estate: estate to pledge
        '''
        self:Estate = estate
        player = sender
        self._pledge(player)

    @staticmethod
    @ev.event_to_estate_rebuy.connect
    def event_handler_rebuy(sender: itf.IEstateForPlayer, estate):
        '''pledge the estate

        :param sender: player to rebuy
        :param estate: estate to rebuy
        '''
        self:Estate = estate
        player = sender
        self._rebuy(player)

    def trigger(self, player: itf.IEstateForPlayer)->None:
        '''override, if owner is not None, take the fee from player
        else ask player whether to buy the place
        '''
        # has owner
        if self.owner:
            # is pledged, escape
            if self.is_pledged:
                logging.info('该地已被 {} 抵押给银行，无法升级和收取地租。'.format(self.owner.name))
                return None
            # take the fee
            elif self.owner != player:
                block_fee = self.block_fee
                logging.info('{} 交给 {} 地租 {}。'.format(player.name, self.owner.name, block_fee))
                self._exchange_money(player, self.owner, block_fee)
            # upgrade
            else:
                ev.event_to_player_upgrade_estate.send(self, owner=player)
        # ask whether to buy
        else:
            ev.event_to_player_buy_place.send(self, buyer=player)

    def __str__(self):
        '''override, display place info
        '''
        owner_name = self.owner.name if self.owner else 'None'
        pledge_state = '抵押' if self.is_pledged else '正常'
        lines = '{}: {}, {}, {}'.format(self.name,
                                        owner_name,
                                        self.current_level,
                                        pledge_state)
        return lines


class EstateBlock:
    '''a block that holds estates with same color
    '''

    def __init__(self, name: str):
        '''init

        :param name: block name
        '''
        self.__name = name
        self.__estates:List[Estate] = []

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
            if estate.owner and estate.owner == owner and not estate.is_pledged:
                block_fee += estate.fee
        return block_fee

    def __len__(self)->int:
        return len(self.__estates)


# project

class Project(BasePlace, itf.IPlayerForProject, itf.IMapForProject):

    def trigger(self, player: itf.IProjectForPlayer)->None:
        '''override take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        if self.owner:
            self._take_effect(player)
        else:
            ev.event_to_player_buy_place.send(self, buyer=player)

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        '''override project is always not equal
        '''
        return False

    def __str__(self):
        '''override display project info
        '''
        owner_name = self.owner.name if self.owner else 'None'
        return '{}: {}'.format(self.name, owner_name)


class ProjectNuclear(Project):
    '''核能发电站'''

    def __init__(self, name: str, pos_in_map: int)->None:
        '''override, init
        '''
        super().__init__(name=name,
                         buy_value=3500,
                         sell_value=3000,
                         pos_in_map=pos_in_map)

    def _take_effect(self, player: itf.IProjectForPlayer)->None:
        '''收取500元，若对方拥有1级/2级/3级地产，额外收取500/1000/1500元。

        :param player: IProjectForPlayer
        '''
        assert self.owner is not None
        if self.owner == player:
            return None
        fine = 500 + 500 * player.estate_max_level
        logging.info('{} 缴付 {} 元给 {}。'.format(player.name, fine, self.owner.name))
        self._exchange_money(player, self.owner, fine)


class ProjectBuilder(Project):
    '''建筑公司'''

    def __init__(self, name: str, pos_in_map: int)->None:
        '''override, init
        '''
        super().__init__(name=name,
                         buy_value=4000,
                         sell_value=3000,
                         pos_in_map=pos_in_map)

    def _buy(self, buyer: itf.IPlaceForPlayer)->None:
        '''override, set the owner to the buyer

        :param buyer: buyer to buy the place
        '''
        super()._buy(buyer)
        self.__register_event_handler()

    def _sell(self, seller: itf.IPlaceForPlayer)->None:
        '''override, remove the owner

        :param seller: seller to sell place
        '''
        super()._sell(seller)
        self.__unregister_event_handler()

    def __register_event_handler(self):
        ev.event_from_estate_upgraded.connect(self.__someone_upgraded_estate)

    def __unregister_event_handler(self):
        ev.event_from_estate_upgraded.disconnect(self.__someone_upgraded_estate)

    def __someone_upgraded_estate(self, sender: Estate)->None:
        '''有人升级房屋，该人需要支付 500 元给 owner of builder

        :param sender: estate that is upgraded
        '''
        estate:Estate = sender
        assert self.owner is not None
        assert estate.owner is not None
        if estate.owner == self.owner:
            return None
        fine = 500
        logging.info('{} 升级地产，需向 {} 支付 {} 元升级费。'.format(estate.owner.name,
                                                                   self.owner.name,
                                                                   fine))
        self._exchange_money(estate.owner, self.owner, fine)

    def _take_effect(self, player: itf.IProjectForPlayer)->None:
        '''每当玩家升级地产时，获得500元。
        当任意玩家到建筑公司时，可将一处地产升一级（需支付升级费用）。

        :param player: IProjectForPlayer
        '''
        logging.info('{} 可选择一处地产升级。'.format(player.name))
        ev.event_to_player_upgrade_any_estate.send(self, player=player)

    def destroy(self)->None:
        '''override, destroy
        '''
        self.__unregister_event_handler()


class ProjectTransportation(Project):
    '''运输公司'''

    def __init__(self, name: str, pos_in_map: int)->None:
        '''override, init
        '''
        super().__init__(name=name,
                         buy_value=3000,
                         sell_value=3000,
                         pos_in_map=pos_in_map)

    def __find_transportaion_amount(self)->int:
        assert self.owner is not None
        player = cast(itf.IProjectForPlayer, self.owner)
        transportations = [project for project in player.projects
                            if isinstance(project, ProjectTransportation)]
        return len(transportations)

    def trigger(self, player: itf.IProjectForPlayer)->None:
        '''override take the effect of the place, triggered by the player

        :param player: IProjectForPlayer
        '''
        if not self.owner:
            ev.event_to_player_buy_place.send(self, buyer=player)
        self._take_effect(player)

    def _take_effect(self, player: itf.IProjectForPlayer)->None:
        '''当你拥有1/2/3项运输项目时，收取500/1000/2000元。
        下回合开始时，你可以放弃投骰子，改为给本项目拥有着500元（无人拥有则给银行），
        立即到任意一个地产处。

        :param player: IProjectForPlayer
        '''
        # take fine if owner is not None and is not the player
        if self.owner and self.owner != player:
            fines = [500, 1000, 2000]
            amount = self.__find_transportaion_amount()
            assert amount >= 1
            fine = fines[amount-1]
            logging.info('{} 缴付 {} 元给 {}。'.format(player.name, fine, self.owner.name))
            self._exchange_money(player, self.owner, fine)
        # ask the player to jump to any estate
        # delay_turns=1 means take action at next turn
        results:List[Tuple[Any, bool]] =\
            ev.event_to_player_jump_to_estate.send(self, player=player, delay_turns=1)
        assert len(results) == 1
        rst:bool = results[0][-1]
        if not rst:
            return None
        fine = 500
        if self.owner is None:
            logging.info('{} 下回合移动位置，支付运输费用 {} 元。'.format(player.name,
                                                                        fine))
            self._subtract_money(player, fine)
        elif self.owner == player:
            logging.info('{} 下回合移动位置。'.format(player.name))
        else:
            logging.info('{} 下回合移动位置，向 {} 支付运输费用 {} 元。'.format(player.name,
                                                                        self.owner.name,
                                                                        fine))
            self._exchange_money(player, self.owner, fine)


class ProjectTvStation(Project):
    '''电视台'''

    def __init__(self, name: str, pos_in_map: int)->None:
        '''override, init
        '''
        super().__init__(name=name,
                         buy_value=3500,
                         sell_value=3000,
                         pos_in_map=pos_in_map)

    def _buy(self, buyer: itf.IPlaceForPlayer)->None:
        '''override, set the owner to the buyer

        :param buyer: buyer to buy the place
        '''
        super()._buy(buyer)
        self.__register_event_handler()

    def _sell(self, seller: itf.IPlaceForPlayer)->None:
        '''override, remove the owner

        :param seller: seller to sell place
        '''
        super()._sell(seller)
        self.__unregister_event_handler()

    def __register_event_handler(self):
        ev.event_from_public_news_or_luck_triggered.connect(self.__someone_triggered_news_or_luck)

    def __unregister_event_handler(self):
        ev.event_from_public_news_or_luck_triggered.disconnect(self.__someone_triggered_news_or_luck)

    def __someone_triggered_news_or_luck(self, sender: Any)->None:
        '''当任何人走到运气和新闻时，你获得500元奖励。

        :param sender: not used
        '''
        assert self.owner is not None
        gain = 500
        self._add_money(self.owner, gain)
        logging.info('新闻 或 运气 被触发，{} 获得 {} 元。'.format(self.owner.name,
                                                                 gain))

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''当任何人走到运气和新闻时，你获得500元奖励。

        :param player: IProjectForPlayer
        '''
        pass

    def destroy(self)->None:
        '''override, destroy
        '''
        self.__unregister_event_handler()

class ProjectSewerage(Project):
    '''污水处理厂'''

    def __init__(self, name: str, pos_in_map: int)->None:
        '''override, init
        '''
        super().__init__(name=name,
                         buy_value=3000,
                         sell_value=3000,
                         pos_in_map=pos_in_map)

    def _take_effect(self, player: itf.IProjectForPlayer):
        '''收取500元，若对方每拥有3块地产，额外收取500元。

        :param player: IProjectForPlayer
        '''
        assert self.owner is not None
        if self.owner == player:
            return None
        estate_amount = len(player.estates)
        fine = 500 + 500 * math.floor(estate_amount / 3)
        logging.info('{} 缴付 {} 元给 {}。'.format(player.name, fine, self.owner.name))
        self._exchange_money(player, self.owner, fine)
