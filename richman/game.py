# -*- coding: utf-8 -*
'''hold the whole game
'''
from richman.base import BasePlace, BaseMap
from richman.player import PlayerImplement


class PlayerNamesDuplicatedException(Exception):
    def __init__(self, *args):
        super().__init__("该玩家已经存在！")


class GameImplement:

    __players = []
    __player_index = 0  # 当前 player index
    
    def __init__(self, map: BaseMap,
                 player_names: list,
                 money: int):
        '''init

        :param map: 
        :param player_names: player names without duplicate
        :param money: init money of players
        '''
        self.__map = map
        self.__players = []
        self.__player_index = 0
        self._build_players(player_names, money)

    @property
    def map(self):
        return self.__map
    @property
    def players(self):
        return self.__players
    @property
    def current_player(self):
        return self.__players[self.__player_index]

    def _build_players(self, player_names: list, money: int):
        if len(set(player_names)) != len(player_names):
            raise PlayerNamesDuplicatedException()
        for name in player_names:
            player = PlayerImplement(name=name, money=money, map=self.map)
            self.__players.append(player)

    def play(self):
        '''进行游戏，下个人掷骰子，并按效果结算
        '''
        self.current_player.play()
