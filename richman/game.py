# -*- coding: utf-8 -*
'''hold the whole game
'''
import logging

import richman.interface as itf 


class GameImplement:

    __player_index = 0  # 当前 player index
    __players_in_game = []
    __players_all = []  # 所有玩家
    __players_banckrupted = []  # 结束游戏的玩家

    def __init__(self, map, players: list):
        '''init

        :param map: 
        :param player_names: list of BasePlayer
        '''
        self.__map = map
        self.__player_index = 0
        self.__players_in_game = players
        self.__players_all = players
        self.__players_banckrupted = []
        self._add_players_into_map(map, players)

    @property
    def map(self):
        return self.__map
    @property
    def players(self):
        return self.__players_all
    @property
    def players_in_game(self):
        return self.__players_in_game
    @property
    def players_banckrupted(self):
        return self.__players_banckrupted

    def _add_players_into_map(self, map, players: itf.IGamePlayer):
        '''add players into map

        :param map: map
        :param players: players
        '''
        for player in players:
            player.add_to_map(map)

    def _remove_players_banckrupted(self, players_banckrupted: list):
        '''remove current player from __players_in_game list

        :param players_banckrupted: list of banckrupted player
        '''
        for player in players_banckrupted:
            self.__players_in_game.remove(player)
            self.__players_banckrupted.append(player)

    def _display_players_info(self):
        for player in self.players:
            logging.info('参赛者信息：{}'.format(player))

    __step = 0
    def _run_one_step(self):
        '''run one step of the game, which means every player run once

        :note: banckrupted players is remove from players list
        '''
        logging.info('第 {} 回合开始：'.format(self.__step))
        players_banckrupted = []
        for player in self.players:
            player.play()
            if player.is_banckrupted:
                logging.info('{} 破产。'.format(player.name))
                players_banckrupted.append(player)
        self._remove_players_banckrupted(players_banckrupted)
        self._display_players_info()
        self.__step += 1

    def run(self):
        '''run the game and show results of each step
        '''
        while len(self.players) > 1:
            self._run_one_step()
        logging.info('{} 获得比赛胜利！'.format(self.players_in_game[0].name))
