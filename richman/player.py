# -*- coding: utf-8 -*
'''player
'''
import random
import datetime
import logging

import richman.interface as itf
import richman.event as ev


class BasePlayer(itf.IGameForPlayer, itf.IMapForPlayer,
                 itf.IEstateForPlayer, itf.IProjectForPlayer):

    def __init__(self, event_manager: itf.IForEventManager,
                 name: str, money: int,
                 map:itf.IPlayerForMap = None):
        '''init

        :param event_manager: event manager interface
        :param name: player name
        :param money: player's init money
        :param map: default is None
        '''
        self.__event_manager = event_manager
        self.__name = name
        assert money > 0, '初始资金必须大于零。'
        self.__money = money
        self.__map = map
        # init others
        self._estates = []
        self._projects = []
        self.__pos = 0
        random.seed(datetime.datetime.now())
        self.__is_making_money = False  # 防止一个 make_money() 过程中多次调用该函数
                                        # event_handler_add_money() 中使用

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
    def map(self, value: itf.IPlayerForMap):
        self.__map = value
    @property
    def pos(self):
        return self.__pos
    @pos.setter
    def pos(self, value: int):
        self.__pos = value % len(self.__map)
    @property
    def estates(self):
        return self._estates
    @property
    def projects(self):
        return self._projects
    @property
    def estate_max_level(self):
        '''return the max level of all the estate the player has
        '''
        if not self.estates:
            return 0
        levels = (estate.current_level for estate in self.estates
                    if isinstance(estate, itf.IPlayerForEstate))
        return max(levels)

    def _dice(self)->int:
        return random.randrange(1,7)
    
    def _remove_place(self, place: itf.IPlayerForPlace):
        '''remove the place from self._estates or self._projects

        :param place: estate or project
        '''
        if isinstance(place, itf.IPlayerForEstate):
            self._estates.remove(place)
        elif isinstance(place, itf.IPlayerForProject):
            self._projects.remove(place)
        else:
            raise RuntimeError('参数类型不正确。')

    def add_to_map(self, map: itf.IPlayerForMap):
        '''add player to map

        :param map: map
        '''
        self.__map = map

    def play(self, reverse=False):
        '''进行下一步游戏

        :param reverse: 是否后退标志
        '''
        step = self._dice()
        logging.info('{} 掷出 {} 点。'.format(self.name, step))
        if reverse:
            step = 0 - step
        self.pos += step
        self.map.trigger(self)

    def _add_money(self, delta: int):
        '''change the player's money

        :param delta: amount of change, minus means subtraction
        '''
        self.__money += delta
        if self.__money < 0 and not self.__is_making_money:
            self.__is_making_money = True
            self._make_money()
            self.__is_making_money = False

    def event_handler_add_money(self, event: ev.EventToPlayerAddMoney):
        '''change the player's money

        :param event: EventToPlayerAddMoney with delta of money
        '''
        self._add_money(event.delta)

    def event_handler_move_to(self, event: ev.EventToPlayerMoveTo):
        '''move player to pos

        :param event: EventToPlayerMoveTo with pos to move
        '''
        self.pos = event.pos

    def event_handler_buy_decision(self, event: ev.EventToPlayerBuyPlace):
        '''decide whether to buy the place

        :param event: EventToPlayerBuyPlace with place to buy
        '''
        place = event.place
        if self._make_decision_buy(place):
            if isinstance(place, itf.IPlayerForProject):
                self._projects.append(place)
            elif isinstance(place, itf.IPlayerForEstate):
                self._estates.append(place)
            else:
                raise RuntimeError('参数 place 必须是 Estate 或者 Project 类型')
            self._add_money(-place.buy_value)
            self.__event_manager.send(ev.EventToPlaceBuy(place.name, self))

    def event_handler_upgrade_decision(self, event: ev.EventToPlayerUpgradeEstate):
        '''decide whether to upgrade the place

        :param event: IPlayerForEstate with place to buy
        '''
        estate = event.estate
        if self._make_decision_upgrade(estate):
            self._add_money(-estate.upgrade_value)
            self.__event_manager.send(ev.EventToEstateUpgrade(estate.name, self))

    def event_handler_jump_to_estate_decision(self, event: ev.EventToPlayerJumpToEstate):
        '''select which estate to go when jump is needed

        :param event: event with no other info
        '''
        self.pos = self._make_decision_jump_to_estate()

    def event_handler_upgrade_any_estate(self, event: ev.EventToPlayerUpgradeAnyEstate):
        '''upgrade and estate that belongs to the player

        :param event: event with no other info
        '''
        estate = self._make_decision_upgrade_any_estate()
        if estate:
            self._add_money(-estate.upgrade_value)
            self.__event_manager.send(ev.EventToEstateUpgrade(estate.name, self))

    def _make_money(self):
        '''make money my pledging or selling,
        to make player's money more than zero
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_buy(self, place: itf.IPlayerForPlace)->bool:
        '''decide whether to buy the place

        :param place: IPlayerForPlace
        :return: True if buy the place
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_upgrade(self, place: itf.IPlayerForEstate):
        '''decide whether to upgrade the place

        :param place: IPlayerForEstate
        :return: True if upgrade
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_jump_to_estate(self)->int:
        '''select which estate to go when jump is needed

        :return: position of estate to jump
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_upgrade_any_estate(self)->itf.IPlayerForEstate:
        '''upgrade and estate that belongs to the player

        :return: estate to upgrade, or None for not upgrade
        '''
        raise NotImplementedError('override is needed.')

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display player info
        '''
        projects_info = [str(project) for project in self.projects]
        estates_info = [str(estate) for estate in self.estates]
        lines = r'姓名: {}，现金: {}，地产: {}，项目：{}。'.format(self.name, self.money,
                                                                 estates_info, projects_info)
        return lines


class PlayerSimple(BasePlayer):

    __is_banckrupted = False
    @property
    def is_banckrupted(self):
        return self.__is_banckrupted

    def __pledge_for_money(self)->bool:
        '''pledge for money
        
        :return: True if money is enough
        '''
        for estate in self.estates:
            if not estate.is_pledged:
                self.__event_manager.send(ev.EventToEstatePledge(estate.name, self))
                self._add_money(estate.pledge_value)
                if self.money > 0:
                    return True
        else:
            return False

    def __sell_place(self, places: list)->int:
        ''' self the places with generator

        :param places: list of IPlayerForPlace
        :return: the player's money after sold out
        '''
        for place in places:
            self.__event_manager.send(ev.EventToPlaceSell(place.name, self))
            self._add_money(place.sell_value)
            self._remove_place(place)
            yield self.money
    
    def __sell_for_money(self)->bool:
        '''sell for money
        
        :return: True if money is enough
        '''
        # sell estate
        for money in self.__sell_place(self._estates):
            if money > 0:
                return True
        # sell project
        for money in self.__sell_place(self._projects):
            if money > 0:
                return True
        # all places is sold out, but still money is below zero
        return False

    def _make_money(self):
        '''make money my pledging or selling,
        to make player's money more than zero
        '''
        # pledge for money
        if self.__pledge_for_money():
            return None
        # sell for money
        if self.__sell_for_money():
            return None
        # banckrupt
        self.__is_banckrupted = True

    def _make_decision_buy(self, place: itf.IPlayerForPlace)->bool:
        '''decide whether to buy the place

        :param place: IPlayerForPlace
        :return: True if buy the place
        '''
        if self.money > place.buy_value:
            return True
        else:
            return False

    def _make_decision_upgrade(self, estate: itf.IPlayerForEstate)->bool:
        '''decide whether to upgrade the estate

        :param estate: IPlayerForPlace
        :return: True if upgrade
        '''
        if (self.money > estate.upgrade_value
                and not estate.is_level_max):
            return True
        else:
            return False

    def _make_decision_jump_to_estate(self)->int:
        '''select which estate to go when jump is needed

        :return: position of estate to jump
        '''
        for index, item in enumerate(self.map.items):
            if (isinstance(item, itf.IPlayerForEstate)
                    and item.pledge_value is not None):
                return index
        else:
            raise RuntimeError('map {} 中没有设置地产！'.format(self.map.name))

    def _make_decision_upgrade_any_estate(self)->itf.IPlayerForEstate:
        '''upgrade and estate that belongs to the player

        :return: estate to upgrade, or None for not upgrade
        '''
        estates_need_upgrade = [estate for estate in self.estates
                                    if not estate.is_level_max]
        if estates_need_upgrade:
            return estates_need_upgrade[0]
        else:
            return None


class PlayerPerson(BasePlayer):
    pass


class PlayerCpu(BasePlayer):
    pass