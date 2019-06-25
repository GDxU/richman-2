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
from richman.place import Estate, EstateBlock, Project


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

def color_name(item: Any)->str:
    return '%s%s%s%s' % (Fore.YELLOW, Back.BLUE, item, Style.RESET_ALL)

def color_place(item: Any)->str:
    return '%s%s%s%s' % (Fore.YELLOW, Back.GREEN, item, Style.RESET_ALL)

def color_num(item: Any)->str:
    # return '%s%s%s%s' % (Fore.GREEN, Back.BLUE, item, Style.RESET_ALL)
    return str(item)


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

    def unregister(self):
        ev.event_from_map_finish.disconnect(self.event_from_map_finish)
        ev.event_from_map_start_round.disconnect(self.event_from_map_start_round)
        ev.event_from_player_start_turn.disconnect(self.event_from_player_start_turn)
        ev.event_from_player_finish_turn.disconnect(self.event_from_player_finish_turn)
        ev.event_to_display_list_of_dict.disconnect(self.event_to_display_list_of_dict)

    def event_from_map_start_round(self, sender: BaseMap)->None:
        print('\n\n第 {} 回合：'.format(color_num(self.map.round)))
        players:List[BasePlayer] = cast(List[BasePlayer], self.map.players_in_game)
        for player in players:
            print('{} 在 {} ：'.format(color_name(player.name),
                                       color_place(self.map.items[player.pos].name)))
            display_player_info(player)

    def event_from_map_finish(self, sender: BaseMap)->None:
        map = sender
        players:List[BasePlayer] = cast(List[BasePlayer], map.players)
        assert map.winner is not None
        print('游戏结束，恭喜 {} 获得比赛胜利！'.format(color_name(map.winner.name)))
        print('比赛结果：')
        for player in players:
            display_player_info(player)
            print()
        input()

    def event_from_player_start_turn(self, sender: BasePlayer)->None:
        '''turn start
        '''
        player = sender
        print('\n{}（{}） 开始行动。'.format(color_name(player.name),
                                            color_place(self.map.items[player.pos].name)))

    def event_from_player_finish_turn(self, sender: BasePlayer)->None:
        '''turn finish
        '''
        player = sender
        print('{} 行动结束。'.format(color_name(player.name)), end='')
        input()

    def event_to_display_list_of_dict(self, sender,
                                      table: List[List[str]],
                                      header:List[str] = None)->None:
        display_list_of_dict(table, header)

    def destroy(self):
        self.unregister()