# -*- coding: utf-8 -*
'''display the game info in command line
'''
from typing import Any, List, Tuple, Dict, Optional, cast

from tabulate import tabulate  # type: ignore

import richman.event as ev
from richman.map import BaseMap
from richman.player import BasePlayer
from richman.place import Estate, EstateBlock, Project


# def split_list_with_width(src: list, width: int)->list:
#     '''split list to lists if the width exceeds

#     :param src: source list to split
#     :param width: width to split with
#     '''
#     rst = []
#     for start_index in range(0, len(src), width):
#         stop_index = start_index + width
#         if stop_index < len(src):
#             rst.append(src[start_index:stop_index])
#         else:
#             rst.append(src[start_index:])
#     return rst

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
    # lines = tabulate(table, header, showindex='always', tablefmt="grid")
    lines = tabulate(table, header, showindex='always', tablefmt="psql")
    print(lines)


class CmdlineDisplay:

    def __init__(self):
        self.register()

    def register(self):
        ev.event_from_map_finish.connect(self.event_from_map_finish)
        ev.event_from_map_start_round.connect(self.event_from_map_start_round)
        ev.event_to_display_list_of_dict.connect(self.event_to_display_list_of_dict)

    def unregister(self):
        ev.event_from_map_finish.disconnect(self.event_from_map_finish)
        ev.event_from_map_start_round.disconnect(self.event_from_map_start_round)
        ev.event_to_display_list_of_dict.disconnect(self.event_to_display_list_of_dict)

    def event_from_map_start_round(self, sender: BaseMap)->None:
        map = sender
        print('第 {} 回合。'.format(map.round))
        players:List[BasePlayer] = cast(List[BasePlayer], map.players_in_game)
        for player in players:
            print('{} 在 {} ：'.format(player.name, map.items[player.pos].name))
            display_player_info(player)

    def event_from_map_finish(self, sender: BaseMap)->None:
        map = sender
        players:List[BasePlayer] = cast(List[BasePlayer], map.players)
        assert map.winner is not None
        print('游戏结束，恭喜 {} 获得比赛胜利！'.format(map.winner.name))
        print('比赛结果：')
        for player in players:
            display_player_info(player)
            print()

    def event_to_display_list_of_dict(self, sender,
                                      table: List[List[str]],
                                      header:List[str] = None)->None:
        display_list_of_dict(table, header)

    def destroy(self):
        self.unregister()