# -*- coding: utf-8 -*
'''display the game info in command line
'''
from typing import List, Tuple, Optional, cast

from tabulate import tabulate  # type: ignore

import richman.event as ev
from richman.map import BaseMap
from richman.player import BasePlayer
from richman.place import Estate, EstateBlock, Project


def display_player_info(player: BasePlayer):
    header = ["姓名", "现金", "总资产", "不动产", "等级", "状态", "收费", "区域收费"]
    RowTyping = Tuple[Optional[str], Optional[str],
                      Optional[str], Optional[str],
                      Optional[int], Optional[str],
                      Optional[str], Optional[str]]
    table:List[RowTyping] = []
    table.append((player.name, '{:,}'.format(player.money),
                  '{:,}'.format(player.total_asset),
                  None, None, None, None, None))
    estates:List[Estate] = cast(List[Estate], player.estates)
    for estate in estates:
        table.append((None, None, None,
                      estate.name, estate.current_level,
                      '抵押' if estate.is_pledged else '正常',
                      estate.fee,
                      '{:,}'.format(estate.block_fee)))
    projects:List[Project] = cast(List[Project], player.projects)
    for project in projects:
        table.append((None, None,
                      None, project.name,
                      None, None, None, None))
    display = tabulate(table, header, showindex='always', tablefmt="grid")
    print(display)


class CmdlineDisplay:

    def __init__(self):
        self.register()

    def register(self):
        ev.event_from_map_finish.connect(self.event_from_map_finish)
        ev.event_from_map_start_round.connect(self.event_from_map_start_round)

    def unregister(self):
        ev.event_from_map_finish.disconnect(self.event_from_map_finish)
        ev.event_from_map_start_round.disconnect(self.event_from_map_start_round)

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

    def destroy(self):
        self.unregister()