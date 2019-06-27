# -*- coding: utf-8 -*
'''公用土地类，例如 新闻，公园 等无法买卖的公共地方
'''
from typing import Any, List, Dict, Optional
import logging

import richman.event as ev
import richman.interface as itf


class BasePublic(itf.IMapForPublic,  itf.IPlayerForPublic):
    
    def __init__(self, name: str, pos_in_map: int)->None:
        self.__name:str = name
        self.__pos_in_map = pos_in_map

    @property
    def name(self)->str:
        return self.__name
    @property
    def pos_in_map(self)->int:
        return self.__pos_in_map

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''trigger the effect of the item in the map

        :param player: the player that trigger the effect
        '''
        raise NotImplementedError('override is needed.')

    def destroy(self)->None:
        '''destroy
        '''
        pass

    def __eq__(self, obj):
        return self.name == obj.name

    def __str__(self):
        return self.name


class PublicStart(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)

    @staticmethod
    @ev.event_from_player_pass_start_line.connect
    def event_handler_add_money_when_player_pass_start_line(sender: itf.IPublicForPlayer)->None:
        '''经过时领取奖励4000元，

        :param sender: the player that trigger the effect
        '''
        player = sender
        gain = 4000
        logging.info('{} 经过起点，得到资金 {} 元。'.format(player.name, gain))
        ev.event_to_player_add_money.send(None, player=player, money_delta=gain)

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''经过时领取奖励4000元，
        若刚好到达起点，可将自己任意一处地产升一级（仍需支付升级费用）。

        :param player: the player that trigger the effect
        '''
        logging.info('{} 可选择一处地产升级。'.format(player.name))
        ev.event_to_player_upgrade_any_estate.send(self, player=player)


class PublicNews(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''抽取1张新闻卡。

        :param player: the player that trigger the effect
        '''
        logging.info('{} 抽取一张新闻卡。'.format(player.name))
        ev.event_from_public_news_or_luck_triggered.send(self)

class PublicPrison(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)
        # prisoner struct: list[player, days left in prison]
        self.__prisoners: Dict[str, int] = {}

    def __register_event_handler(self)->None:
        ev.event_from_player_start_turn.connect(self.__prison_day_count_down)
        ev.event_from_player_block_before_turn.connect(self.__block_prisoner_turn)
        ev.event_from_player_block_before_add_money.connect(self.__block_prisoner_take_money)

    def __unregister_event_handler(self)->None:
        ev.event_from_player_start_turn.disconnect(self.__prison_day_count_down)
        ev.event_from_player_block_before_turn.disconnect(self.__block_prisoner_turn)
        ev.event_from_player_block_before_add_money.disconnect(self.__block_prisoner_take_money)

    def __prison_day_count_down(self, sender: itf.IPublicForPlayer)->None:
        '''count down days in prison,
        remove player if days left in prison is zero after count down

        :param sender: player to start the turn
        '''
        player:itf.IPublicForPlayer = sender
        name = player.name
        if name not in self.__prisoners:
            return None
        if self.__prisoners[name] == 0:
            logging.info('{} 出狱。'.format(player.name))
            self.__prisoners.pop(name)
        else:
            self.__prisoners[name] -= 1

    def __block_prisoner_turn(self, sender: itf.IPublicForPlayer)->bool:
        '''block the player turn if the player in the prison

        :param sender: player the trigger the event
        :return: True if need to block the action
        '''
        player:itf.IPublicForPlayer = sender
        if not self.__prisoners:
            self.__unregister_event_handler()
        to_block =  player.name in self.__prisoners
        if to_block:
            logging.info('{} 入狱中，无法移动。'.format(player.name))
        return to_block

    def __block_prisoner_take_money(self, sender: itf.IPublicForPlayer,
                                    source: Any,
                                    money_delta)->bool:
        '''block the positive add money if the player is in prison
        and the negtive add money if the place owner is in prison

        :param sender: player the trigger the event
        :param source: the sender that trigger the "add_money" event
        :param money_delta: money to add
        :return: True if need to block the action
        '''
        player:itf.IPublicForPlayer = sender
        # player is in prison, block if money_delta is positive
        if player.name in self.__prisoners and money_delta > 0:
            logging.info('{} 入狱中，无法收取地租（奖励）。'.format(player.name))
            return True
        # the source belongs to prisoner, block if money_delta is negtive
        elif (isinstance(source, itf.IPublicForPlace)
                and source.owner
                and source.owner.name in self.__prisoners
                and money_delta < 0):
            logging.info('{} 入狱中，无需支付地租（费用）。'.format(source.owner.name))
            return True
        # do not block
        else:
            return False

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''停留一回合。
        当你在监狱时，不能收取租金或获得任何金钱奖励。

        :param player: the player that trigger the effect
        '''
        logging.info('{} 停留一回合，不能收取租金或奖励。'.format(player.name))
        assert player.name not in self.__prisoners
        self.__prisoners[player.name] = 1
        self.__register_event_handler()

    def destroy(self):
        self.__unregister_event_handler()

class PublicLuck(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''抽取1张运气卡。

        :param player: the player that trigger the effect
        '''
        ev.event_from_public_news_or_luck_triggered.send(self)
        logging.info('{} 抽取一张幸运卡。'.format(player.name))

class PublicStock(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''获得500元，然后额外获得你拥有投资项目数量*500元的奖励。

        :param player: the player that trigger the effect
        '''
        projects_amount = len(player.projects)
        gain = 500 + 500 * projects_amount
        logging.info('{} 有 {} 块项目，获得 {} 元资金。'.format(player.name,
                                                              projects_amount,
                                                              gain))
        ev.event_to_player_add_money.send(self, player=player,
                                          money_delta=gain)

class PublicGotoPrison(BasePublic):
    def __init__(self, name: str, pos_in_map: int,
                 prison_pos: int)->None:
        '''init

        :param name: name of the publick
        :param prison_pos: prison position in the map
        '''
        super().__init__(name, pos_in_map)
        self.__prison_pos = prison_pos

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''立即进入监狱并停留一回合。

        :param player: the player that trigger the effect
        '''
        logging.info('{} 立即进入监狱。'.format(player.name))
        # delay_turns=0 means take action right now
        ev.event_to_player_move_to.send(self, player=player,
                                        pos=self.__prison_pos,
                                        delay_turns=0)

class PublicPark(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''拾到300元。

        :param player: the player that trigger the effect
        '''
        gain = 300
        logging.info('{} 在公园捡到 {} 元。'.format(player.name, gain))
        ev.event_to_player_add_money.send(self, player=player,
                                          money_delta=gain)

class PublicTax(BasePublic):
    def __init__(self, name: str, pos_in_map: int)->None:
        super().__init__(name, pos_in_map)

    def trigger(self, player: itf.IPublicForPlayer)->None:
        '''缴纳每块地产300元税金。

        :param player: the player that trigger the effect
        '''
        estates_amount = len(player.estates)
        fine = 300 * estates_amount
        logging.info('{} 有 {} 块地产，需缴纳 {} 元税金。'.format(player.name,
                                                                estates_amount,
                                                                fine))
        ev.event_to_player_add_money.send(self, player=player,
                                          money_delta=-fine)