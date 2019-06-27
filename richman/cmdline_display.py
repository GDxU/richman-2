# -*- coding: utf-8 -*
'''display the game info in command line
'''
from typing import Any, List, Tuple, Dict, Optional, cast

from tabulate import tabulate  # type: ignore
from colorama import init, Fore, Back, Style  # type: ignore
init()

import richman.event as ev
from richman.map import BaseMap
from richman.player import BasePlayer
from richman.place import BasePlace, Estate, EstateBlock, Project


def display_list_of_dict(table: List[List[str]],
                         header:List[str] = None,
                         width:int = 10)->None:
    '''display with header and table
    '''
    print(tabulate(table, header))  # type: ignore

def display_player_info(player: BasePlayer)->None:
    '''显示参赛者信息
    '''
    header = ["姓名", "现金", "总资产", "不动产", "等级", "状态", "收费", "区域收费"]
    RowTyping = Tuple[Optional[str], Optional[str],
                      Optional[str], Optional[str],
                      Optional[int], Optional[str],
                      Optional[str], Optional[str]]
    table:List[RowTyping] = []
    table.append((player.name, '{:,}'.format(player.money),
                  '{:,}'.format(player.total_asset), None,
                  None, None,
                  None, None))
    estates:List[Estate] = cast(List[Estate], player.estates)
    for estate in estates:
        table.append((None, None,
                      None, estate.name,
                      estate.current_level, '抵押' if estate.is_pledged else '正常',
                      '{:,}'.format(estate.fee), '{:,}'.format(estate.block_fee)))
    projects:List[Project] = cast(List[Project], player.projects)
    for project in projects:
        table.append((None, None,
                      None, project.name,
                      None, None,
                      None, None))
    lines = tabulate(table, header, showindex='always', tablefmt="psql")
    print(lines)

def color_player(player: Any)->str:
    return '%s%s%s%s' % (Fore.YELLOW, Back.GREEN, player.name, Style.RESET_ALL)

def color_place(place: Any)->str:
    return '%s%s%s%s' % (Fore.YELLOW, Back.BLACK, place.name, Style.RESET_ALL)

def color_num(num: int)->str:
    return '%s%s%s%s' % (Fore.BLACK, Back.WHITE,
                         '{:,}'.format(num), Style.RESET_ALL)
    # return str(item)


class CmdlineDisplay:

    def __init__(self, map: BaseMap):
        self.__map = map
        self.register()

    @property
    def map(self)->BaseMap:
        return self.__map

    def register(self):
        ev.event_from_map_finish.connect(self.event_from_map_finish)
        ev.event_from_map_start_round.connect(self.event_from_map_start_round)
        ev.event_from_player_start_turn.connect(self.event_from_player_start_turn)
        ev.event_from_player_finish_turn.connect(self.event_from_player_finish_turn)
        ev.event_to_display_list_of_dict.connect(self.event_to_display_list_of_dict)
        ev.event_from_player_after_dice.connect(self.event_from_player_after_dice)
        ev.event_from_place_bought.connect(self.event_from_place_bought)
        ev.event_from_place_sold.connect(self.event_from_place_sold)

    def unregister(self):
        ev.event_from_map_finish.disconnect(self.event_from_map_finish)
        ev.event_from_map_start_round.disconnect(self.event_from_map_start_round)
        ev.event_from_player_start_turn.disconnect(self.event_from_player_start_turn)
        ev.event_from_player_finish_turn.disconnect(self.event_from_player_finish_turn)
        ev.event_to_display_list_of_dict.disconnect(self.event_to_display_list_of_dict)
        ev.event_from_player_after_dice.disconnect(self.event_from_player_after_dice)
        ev.event_from_place_bought.disconnect(self.event_from_place_bought)
        ev.event_from_place_sold.disconnect(self.event_from_place_sold)

    def destroy(self):
        self.unregister()

    # handler utillities

    def event_to_display_list_of_dict(self, sender,
                                      table: List[List[str]],
                                      header:List[str] = None)->None:
        display_list_of_dict(table, header)

    # handler from map

    def event_from_map_start_round(self, sender: BaseMap)->None:
        print('\n\n第 {} 回合：'.format(color_num(self.map.round)))
        players:List[BasePlayer] = cast(List[BasePlayer], self.map.players_in_game)
        for player in players:
            place = self.map.items[player.pos]
            print('{} @{} ：'.format(color_player(player),
                                       color_place(place)))
            display_player_info(player)

    def event_from_map_finish(self, sender: BaseMap)->None:
        map = sender
        players:List[BasePlayer] = cast(List[BasePlayer], map.players)
        assert map.winner is not None
        print('\n\n游戏结束，恭喜 {} 获得比赛胜利！'.format(color_player(map.winner)))
        print('比赛结果：')
        for player in players:
            display_player_info(player)
            print()
        input()

    # handler from player

    def event_from_player_start_turn(self, sender: BasePlayer)->None:
        '''turn start
        '''
        player = sender
        place = self.map.items[player.pos]
        print('\n{} @{} {} 开始行动。'.format(color_player(player),
                                                  color_place(place),
                                                  color_num(player.money)))

    def event_from_player_finish_turn(self, sender: BasePlayer)->None:
        '''turn finish
        '''
        player = sender
        print('{} 行动结束。'.format(color_player(player)))
        input()

    def event_from_player_after_dice(self, sender: BasePlayer, dice_num: int)->None:
        '''display dice num and dist
        '''
        player = sender
        place = self.map.items[player.pos]
        print('{} 掷了 {} 点，走到 {} 。'.format(color_player(player),
                                                color_num(dice_num),
                                                color_place(place)))

    # handler from place
    def event_from_place_bought(self, sender: BasePlace)->None:
        '''place is bought
        '''
        place = sender
        print('{} 购买 {}，花费 {} 元。'.format(color_player(place.owner),
                                                          color_place(place),
                                                          color_num(place.buy_value)))

    def event_from_place_sold(self, sender: BasePlace)->None:
        '''place is sold
        '''
        place = sender
        print('{} 变卖地 {}，获得 {} 元。'.format(color_player(place.owner),
                                                          color_place(place),
                                                          color_num(place.sell_value)))
