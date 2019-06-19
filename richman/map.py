# -*- coding: utf-8 -*
'''map
'''
import typing
import logging
import pickle
import os

import richman.interface as itf


class BaseMap(itf.IPlayerForMap, itf.IGameForMap):

    def __init__(self, name: str):
        '''init

        :param name: map name
        '''
        self.__name = name
        # init others
        self.__items:typing.List[itf.IMapForItem] = []
        self.__players:typing.List[itf.IMapForPlayer] = []
        self.__players_in_game:typing.List[itf.IMapForPlayer] = []
        self.__players_banckrupted:typing.List[itf.IMapForPlayer] = []
        self.__current_player_index = 0
        self.__round_cnt = 0

    @property
    def name(self)->str:
        return self.__name
    @property
    def items(self)->typing.List[itf.IMapForItem]:
        return self.__items
    @property
    def players(self)->typing.List[itf.IMapForPlayer]:
        return self.__players
    @property
    def players_in_game(self)->typing.List[itf.IMapForPlayer]:
        return self.__players_in_game
    @property
    def players_banckrupted(self)->typing.List[itf.IMapForPlayer]:
        return self.__players_banckrupted
    @property
    def round(self)->int:
        return self.__round_cnt

    def add_items(self, items: typing.List[itf.IMapForItem]):
        if not isinstance(items, list):
            items = [items]
        for item in items:
            assert item not in self.items,\
                'estate names should not be duplicated.'
            self.__items.append(item)

    def add_players(self, players: typing.List[itf.IMapForPlayer]):
        '''add players to map

        :param players: list of players
        '''
        if not isinstance(players, list):
            players = [players]
        for player in players:
            assert player not in self.players,\
                '{} has been existed already.'.format(player.name)
            self.__players.append(player)
            player.map = self
        self.__players_in_game = self.players.copy()

    def load(self, file_path: str):
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

    def save(self, file_path: str):
        '''save map into pickle

        :param file_path: file_path to save
        '''
        map = {}
        map['name'] = self.name
        map['items'] = self.items
        with open(file_path, 'wb') as f:
            pickle.dump(map, f)

    def _display_players_info(self):
        for player in self.players:
            logging.info('参赛者信息：{}'.format(player))

    def _remove_players_banckrupted(self, players_banckrupted: typing.List[itf.IMapForPlayer]):
        '''remove current player from __players_in_game list

        :param players_banckrupted: list of banckrupted player
        '''
        for player in players_banckrupted:
            self.__players_in_game.remove(player)

    def _player_action(self, player: itf.IMapForPlayer):
        pos = player.dice()
        self.items[pos].trigger(player)

    def _run_one_round(self):
        '''run one round of the map, which means every player run once

        :note: banckrupted players is remove from players list
        '''
        logging.info('\n第 {} 回合开始：'.format(self.round))
        players_banckrupted = []
        for player in self.players_in_game:
            self._player_action(player)
            if player.is_banckrupted:
                logging.info('{} 破产。'.format(player.name))
                players_banckrupted.append(player)
        self._remove_players_banckrupted(players_banckrupted)
        self._display_players_info()
        self.__round_cnt += 1

    def run_one_round(self):
        '''run one round of the map, which means every player run once

        :return: False if only one player is left
        '''
        self._run_one_round()
        return len(self.players_in_game) > 1

    def __len__(self):
        return len(self.items)
