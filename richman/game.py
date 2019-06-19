# -*- coding: utf-8 -*
'''hold the whole game
'''
import logging

import richman.interface as itf
import richman.event as ev


class BaseGame:

    def __init__(self, map: itf.IGameForMap, players: list):
        '''init

        :param map: 
        :param player_names: list of BasePlayer
        '''
        self.__map = map
        # init others
        self.map.add_players(players)

    @property
    def map(self):
        return self.__map

    def run(self):
        '''run the game and show results of each step
        '''
        while self.map.run_one_round():
            pass
        logging.info('{} 获得比赛胜利！'.format(self.map.players_in_game[0].name))

class Game(BaseGame):
    pass