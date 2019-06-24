# -*- coding: utf-8 -*
'''hold the whole game
'''
from typing import List
import logging

import richman.interface as itf
import richman.event as ev


class BaseGame:

    def __init__(self, map: itf.IGameForMap,
                 players: List[itf.IGameForPlayer],
                 display_frame = None)->None:
        '''init

        :param map: 
        :param player_names: list of BasePlayer
        :param display_frame: the frame to display the gaming info
        '''
        self.__map = map
        self.__map.add_players(players)
        self.display_frame = display_frame

    @property
    def map(self)->itf.IGameForMap:
        return self.__map

    def run(self):
        '''run the game and show results of each step
        '''
        while self.map.run_one_round():
            pass
        self.destroy()

    def destroy(self):
        self.map.destroy()
        if self.display_frame:
            self.display_frame.destroy()

class Game(BaseGame):
    pass