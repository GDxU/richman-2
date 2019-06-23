# -*- coding: utf-8 -*
'''player
'''
from typing import Any, List, Dict, Tuple, Iterable, Optional, cast
import random
import datetime
import logging

import richman.interface as itf
import richman.event as ev


class BasePlayer(itf.IGameForPlayer, itf.IMapForPlayer,
                 itf.IEstateForPlayer, itf.IProjectForPlayer,
                 itf.IPlaceForPlayer):

    def __init__(self, name: str, money: int)->None:
        '''init

        :param name: player name
        :param money: player's init money
        '''
        self.__name:str = name
        assert money > 0, '初始资金必须大于零。'
        self.__money:int = money
        self.__map:Optional[itf.IPlayerForMap] = None
        # init others
        self._estates:List[itf.IPlayerForEstate] = []
        self._projects:List[itf.IPlayerForProject] = []
        self.__pos:int = 0
        self.__pos_queue:List[Dict[str, int]] = []
        random.seed(datetime.datetime.now())
        self.__is_making_money:bool = \
            False  # 防止一个 make_money() 过程中多次调用该函数
            # __event_handler_add_money() 中使用

    @property
    def name(self)->str:
        return self.__name
    @property
    def is_banckrupted(self)->bool:
        raise NotImplementedError('need override.')
    @property
    def money(self)->int:
        return self.__money
    @property
    def map(self)->Optional[itf.IPlayerForMap]:
        return self.__map
    @property
    def pos(self)->int:
        return self.__pos
    @pos.setter
    def pos(self, value: int):
        assert self.map is not None, 'player is not added to any map, yet.'
        self.__pos = value % len(self.map)
    @property
    def estates(self)->List[itf.IPlayerForEstate]:
        return self._estates
    @property
    def projects(self)->List[itf.IPlayerForProject]:
        return self._projects
    @property
    def estate_max_level(self)->int:
        '''return the max level of all the estate the player has
        '''
        if not self.estates:
            return 0
        levels = (estate.current_level for estate in self.estates
                    if isinstance(estate, itf.IPlayerForEstate))
        return max(levels)

    def add_map(self, map: itf.IPlayerForMap)->None:
        '''add map to player

        :param map: map with IPlayerForMap interface
        '''
        assert self.map is None
        self.__map = map

    def _dice(self)->int:
        dice_num = random.randrange(1,7)
        logging.info('{} 掷出 {} 点。'.format(self.name, dice_num))
        return dice_num

    def _remove_place(self, places: List[itf.IPlayerForPlace])->None:
        '''remove the place from self._estates or self._projects

        :param places: list of estate or project
        '''
        if not isinstance(places, list):
            places = [cast(itf.IPlayerForPlace, places)]
        for place in places:
            if isinstance(place, itf.IPlayerForEstate):
                self._estates.remove(place)
            elif isinstance(place, itf.IPlayerForProject):
                self._projects.remove(place)
            else:
                raise RuntimeError('参数类型不正确。')

    def _add_money(self, delta: int)->int:
        '''change the player's money

        :param delta: amount of change, minus means subtraction
        :return: current money after add action
        '''
        self.__money += delta
        if self.money < 0 and not self.__is_making_money:
            self.__is_making_money = True
            self._make_money()
            self.__is_making_money = False
        return self.money

    def _push_pos(self, pos: int, delay_turns: int)->None:
        '''push the pos, where to direct the player to go, to the queue

        :param pos: next pos the player should stand
        :param delay_turns: the effect takes on after delay_turns of the turns
        :note: (delay_turns = 0) means trigger the map item right now,
               (delay_turns = 1) means trigger the map item at next turn
        '''
        assert delay_turns >= 0, 'delay_turns should be above zero!'
        if delay_turns == 0:
            self.__trigger_map_item(pos)
        else:
            self.__pos_queue.append({'pos': pos, 'delay_turns': delay_turns})

    def _pull_pos(self)->Optional[int]:
        '''push the pos, where to direct the player to go, to the queue

        :return: pos to go, None if no pos in the queue
        '''
        if not self.__pos_queue:
            return None
        pos_with_no_delay:List[Dict[str, int]] = []
        for item in self.__pos_queue:
            item['delay_turns'] -= 1
            assert item['delay_turns'] >= 0, 'delay_turns should be above zero!'
            if item['delay_turns'] == 0:
                pos_with_no_delay.append(item)
        assert len(pos_with_no_delay) <= 1, 'more than one pos signal triggered!'
        if pos_with_no_delay:
            self.__pos_queue.remove(pos_with_no_delay[0])
            return pos_with_no_delay[0]['pos']
        else:
            return None

    @staticmethod
    @ev.event_to_player_add_money.connect
    def __event_handler_add_money(sender: Any,
                                  player,
                                  money_delta: int)->None:
        '''change the player's money

        :param sender: source to add the money
        :param player: player to change the money
        :param money_delta: money to change
        '''
        self:BasePlayer = player
        results:List[Tuple[Any, Optional[bool]]] = \
            ev.event_from_player_block_before_add_money.send(self, 
                                                             source=sender,
                                                             money_delta=money_delta)
        is_blocked = ev.check_event_result_is_true(results)
        if is_blocked is not True:
            self._add_money(money_delta)

    @staticmethod
    @ev.event_to_player_move_to.connect
    def __event_handler_move_to(sender,
                                player,
                                pos: int,
                                delay_turns:int = 0)->None:
        '''move player to pos

        :param sender: not used
        :param player: player to move
        :param pos: position to move to
        :param delay_turns: delay_turns of turns to take effect
        '''
        self:BasePlayer = player
        assert pos is not None
        self._push_pos(pos=pos, delay_turns=delay_turns)

    @staticmethod
    @ev.event_to_player_buy_place.connect
    def __event_handler_buy_decision(sender: itf.IPlayerForPlace,
                                     buyer)->None:
        '''decide whether to buy the place

        :param sender: place to decide to buy
        :param buyer: buyer
        '''
        self:BasePlayer = buyer
        place = sender
        if self._make_decision_buy(place):
            if isinstance(place, itf.IPlayerForProject):
                self._projects.append(place)
            elif isinstance(place, itf.IPlayerForEstate):
                self._estates.append(place)
            else:
                raise RuntimeError('参数 place 必须是 Estate 或者 Project 类型')
            ev.event_to_place_buy.send(self, place=place)

    @staticmethod
    @ev.event_to_player_upgrade_estate.connect
    def __event_handler_upgrade_decision(sender: itf.IPlayerForEstate,
                                         owner)->None:
        '''decide whether to upgrade the place

        :param sender: estate to upgrade
        :param owner: owner of the estate to upgrade
        '''
        self:BasePlayer = owner
        estate = sender
        if self._make_decision_upgrade(estate):
            ev.event_to_estate_upgrade.send(self, estate=estate)

    @staticmethod
    @ev.event_to_player_jump_to_estate.connect
    def __event_handler_jump_to_estate_decision(sender: Any,
                                                player,
                                                delay_turns:int = 0)->bool:
        '''select which estate to go when jump is needed

        :param sender: not used
        :param player: player to jump
        :param delay_turns: delay_turns of turns to take effect
        '''
        self:BasePlayer = player
        pos = self._make_decision_jump_to_estate()
        if pos is not None:
            self._push_pos(pos=pos, delay_turns=delay_turns)
            return True
        else:
            return False

    @staticmethod
    @ev.event_to_player_upgrade_any_estate.connect
    def __event_handler_upgrade_any_estate(sender: Any, player)->None:
        '''upgrade and estate that belongs to the player

        :param sender: not used
        :param player: player to upgrade any estate
        '''
        self:BasePlayer = player
        estate = self._make_decision_upgrade_any_estate()
        if estate and self.money > estate.upgrade_value:
            ev.event_to_estate_upgrade.send(self, estate=estate)

    def _make_money(self)->None:
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

    def _make_decision_upgrade(self, place: itf.IPlayerForEstate)->bool:
        '''decide whether to upgrade the place

        :param place: IPlayerForEstate
        :return: True if upgrade
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_jump_to_estate(self)->Optional[int]:
        '''select which estate to go when jump is needed

        :return: position of estate to jump
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_upgrade_any_estate(self)->Optional[itf.IPlayerForEstate]:
        '''upgrade and estate that belongs to the player

        :return: estate to upgrade, or None for not upgrade
        '''
        raise NotImplementedError('override is needed.')

    def _make_decision_before_dice_start(self)->None:
        '''do something before dice
        '''
        raise NotImplementedError('override is needed.')

    def take_the_turn(self)->None:
        '''take_the_turn
        '''
        # send start_turn event
        ev.event_from_player_start_turn.send(self)
        # check if the turn is blocked
        results:List[Tuple[Any, Optional[bool]]] = \
            ev.event_from_player_block_before_turn.send(self)
        is_blocked = ev.check_event_result_is_true(results)
        if is_blocked is True:
            return None
        # calculate pos
        pos_before_turn = self.pos  # for pass start line check
        pos_in_queue = self._pull_pos()
        if pos_in_queue is not None:
            pos = pos_in_queue
        else:
            self._make_decision_before_dice_start()
            pos = self.pos + self._dice()
        pos_after_turn = pos
        # check if the player passes the start line
        assert self.map is not None
        if (pos_after_turn < pos_before_turn
                and pos_before_turn > 0.5*len(self.map)):
            ev.event_from_player_pass_start_line.send(self)
        # trigger the item
        self.__trigger_map_item(pos)

    def __trigger_map_item(self, pos: int)->None:
        '''trigger the map item action

        :param pos: the position the player go to
        '''
        self.pos = pos
        assert self.map is not None
        item:itf.IMapForItem = self.map.items[self.pos]
        logging.info('{} 走到 {}。'.format(self.name, item.name))
        item.trigger(self)

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        '''display player info
        '''
        projects_info = [str(project) for project in self.projects]
        estates_info = [str(estate) for estate in self.estates]
        lines = (r'姓名: {}，位置: {}，现金: {}，地产: {}，'
                    r'项目：{}。').format(self.name, self.pos, self.money,
                                  estates_info, projects_info)
        return lines


class PlayerSimple(BasePlayer):

    __is_banckrupted = False
    @property
    def is_banckrupted(self)->bool:
        return self.__is_banckrupted

    def __pledge_for_money(self)->bool:
        '''pledge for money
        
        :return: True if money is enough
        '''
        for estate in self.estates:
            if not estate.is_pledged:
                ev.event_to_estate_pledge.send(self, estate=estate)
                if self.money > 0:
                    return True
        else:
            return False

    def __sell_place(self, places: List[itf.IPlayerForPlace])->bool:
        ''' sell the places

        :param places: list of IPlayerForPlace
        :return: True if money is enough
        '''
        def sell_place_iteration(cls: BasePlayer, places_to_sell):
            for place in places_to_sell:
                ev.event_to_place_sell.send(cls, place=place)
                yield (place, cls.money)
        place_to_remove = []
        is_money_enough = False
        for place, money in sell_place_iteration(self, places):
            place_to_remove.append(place)
            if money >= 0:
                is_money_enough = True
                break
        self._remove_place(place_to_remove)
        if is_money_enough:
            return True
        else:
            return False

    def __sell_for_money(self)->bool:
        '''sell for money

        :return: True if money is enough
        '''
        # sell estate
        if self.__sell_place(cast(List[itf.IPlayerForPlace], self.estates)):
            return True
        # sell project
        elif self.__sell_place(cast(List[itf.IPlayerForPlace], self.projects)):
            return True
        # all places is sold out, but still money is below zero
        else:
            return False

    def _make_money(self)->None:
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
        assert self.money < 0
        assert not self.estates
        assert not self.projects
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
        if (self.money > estate.upgrade_value + 1000
                and not estate.is_level_max):
            return True
        else:
            return False

    def _make_decision_jump_to_estate(self)->Optional[int]:
        '''select which estate to go when jump is needed

        :return: position of estate to jump
        '''
        assert self.map is not None
        for estate in self.estates:
            if not estate.is_pledged:
                return self.map.get_item_position(estate)
        else:
            return None

    def _make_decision_upgrade_any_estate(self)->Optional[itf.IPlayerForEstate]:
        '''upgrade and estate that belongs to the player

        :return: estate to upgrade, or None for not upgrade
        '''
        estates_need_upgrade = [estate for estate in self.estates
                                    if not estate.is_level_max]
        for estate in estates_need_upgrade:
            if self.money > estate.upgrade_value + 1000:
                return estate
        else:
            return None

    def _make_decision_before_dice_start(self)->None:
        '''do something before dice
        rebuy if has enough money
        '''
        money_threshold = 10000
        if self.money > money_threshold:
            estates_pledged = [estate for estate in self.estates
                                if estate.is_pledged]
            for estate in estates_pledged:
                if self.money > money_threshold:
                    ev.event_to_estate_rebuy.send(self, estate=estate)


class PlayerPerson(BasePlayer):
    pass


class PlayerCpu(BasePlayer):
    pass