# -*- coding: utf-8 -*
'''hold the whole game
'''
import richman.interface as itf 


class GameImplement:

    __players = []
    __player_index = 0  # 当前 player index
    __players_banckrupted = []  # 结束游戏的玩家

    def __init__(self, map, players: list):
        '''init

        :param map: 
        :param player_names: list of BasePlayer
        '''
        self.__map = map
        self.__players = players
        self.__player_index = 0
        self.__players_banckrupted = []
        self._add_players_into_map(map, players)

    @property
    def map(self):
        return self.__map
    @property
    def players(self):
        return self.__players
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
        '''remove current player from __players list

        :param players_banckrupted: list of banckrupted player
        '''
        for player in players_banckrupted:
            self.__players.remove(player)
            self.__players_banckrupted.append(player)

    def _run_one_step(self):
        '''run one step of the game, which means every player run once

        :note: banckrupted players is remove from players list
        '''
        players_banckrupted = []
        for player in self.players:
            player.play()
            if player.is_banckrupted:
                print('player {} is banckrupted.'.format(player.name))
                players_banckrupted.append(player)
        self._remove_players_banckrupted(players_banckrupted)

    def run(self):
        '''run the game and show results of each step
        '''
        while self.players:
            self._run_one_step()
