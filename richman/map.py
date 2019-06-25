# -*- coding: utf-8 -*
'''map
'''
from typing import Any, List, Dict, Optional, Iterator, cast
import logging
import pickle
import os

import richman.event as ev
import richman.interface as itf


class BaseMap(itf.IPlayerForMap, itf.IGameForMap):

    def __init__(self, name: str):
        '''init

        :param name: map name
        '''
        self.__name = name
        # init others
        self.__items:List[itf.IMapForItem] = []
        self.__players:List[itf.IMapForPlayer] = []
        self.__players_in_game:List[itf.IMapForPlayer] = []
        self.__players_banckrupted:List[itf.IMapForPlayer] = []
        self.__current_player_index = 0
        self.__round_cnt = 0

    @property
    def name(self)->str:
        return self.__name
    @property
    def items(self)->List[itf.IMapForItem]:
        return self.__items
    @property
    def players(self)->List[itf.IMapForPlayer]:
        return self.__players
    @property
    def players_in_game(self)->List[itf.IMapForPlayer]:
        return self.__players_in_game
    @property
    def players_banckrupted(self)->List[itf.IMapForPlayer]:
        return self.__players_banckrupted
    @property
    def round(self)->int:
        return self.__round_cnt
    @property
    def winner(self)->Optional[itf.IMapForPlayer]:
        if len(self.players_in_game) > 1:
            return None
        else:
            return self.players_in_game[0]

    def get_item_position(self, item: Any)->int:
        '''get the position of the item in the map
        :param item: item in the map
        '''
        for pos, item_in_map in enumerate(self.items):
            if item == item_in_map:
                return pos
        else:
            raise RuntimeError('{} is not in the map'.format(item))

    def add_items(self, items: List[itf.IMapForItem]):
        if not isinstance(items, list):
            items = [cast(itf.IMapForItem, items)]
        for item in items:
            if isinstance(item, itf.IMapForEstate):
                assert item not in self.items,\
                    '%s estate should not be duplicated.' % item.name
            self.__items.append(item)

    def add_players(self, players: List[itf.IMapForPlayer]):
        '''add players to map

        :param players: list of players
        '''
        if not isinstance(players, list):
            players = [cast(itf.IMapForPlayer, players)]
        for player in players:
            assert player not in self.players,\
                '{} has been existed already.'.format(player.name)
            self.__players.append(player)
            player.add_map(self)
        self.__players_in_game = self.players.copy()

    def load(self, file_path: str)->None:
        '''load map from pickle

        :param file_path: file_path to load
        '''
        assert os.path.exists(file_path),\
            '用于读取 map 的文件不存在：{}。'.format(file_path)
        with open(file_path, 'rb') as f:
            map = pickle.load(f)
        assert map, '读取或解析失败：{}。'
        self.__name = map['name']
        self.__items = map['items']

    def save(self, file_path: str)->None:
        '''save map into pickle

        :param file_path: file_path to save
        '''
        map:Dict[str, Any] = {}
        map['name'] = self.name
        map['items'] = self.items
        with open(file_path, 'wb') as f:
            pickle.dump(map, f)

    def _display_players_info(self)->None:
        logging.info('\n参赛者信息：')
        for player in self.players:
            logging.info('{}'.format(player))

    def _remove_players_banckrupted(self)->None:
        '''remove banckrupted player from __players_in_game list
        '''
        for player in self.players_banckrupted:
            if player in self.players_in_game:
                self.__players_in_game.remove(player)

    def run_one_player_turn(self)->bool:
        '''run one player's turn

        :return: False if all players has done the turn
        '''
        # pick the current player
        player = self.players_in_game[self.__current_player_index]
        # play the turn
        logging.info('\n{}：'.format(player.name))
        player.take_the_turn()
        if player.is_banckrupted:
            logging.info('{} 破产。'.format(player.name))
            self.__players_banckrupted.append(player)
        # move to next player
        self.__current_player_index += 1
        # if all players are done, do the remove operation
        if self.__current_player_index >= len(self.players_in_game):
            self.__current_player_index = 0
            self._remove_players_banckrupted()
            return False
        else:
            return True

    def _run_one_round(self)->None:
        '''run one round of the map, which means every player run once

        :note: banckrupted players is remove from players list
        '''
        # logging.info('\n\n第 {} 回合开始：'.format(self.round))
        # self._display_players_info()
        ev.event_from_map_start_round.send(self)
        while self.run_one_player_turn():
            pass
        self.__round_cnt += 1
        ev.event_from_map_finish_round.send(self)

    def run_one_round(self)->bool:
        '''run one round of the map, which means every player run once

        :return: False if only one player is left
        '''
        self._run_one_round()
        if self.winner:
            ev.event_from_map_finish.send(self)
            logging.info('{} 获得比赛胜利！'.format(self.winner.name))
            self._display_players_info()
            return False
        else:
            return True

    def destroy(self)->None:
        '''destroy
        '''
        for item in self.items:
            item.destroy()

    def __len__(self):
        return len(self.items)
