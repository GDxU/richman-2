# -*- coding: utf-8 -*
'''hold the whole game
'''
from collections import deque
from typing import Any, List
import logging

import richman.interface as itf
import richman.event as ev
import richman.utility as util


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
        self.__transaction = util.Transaction(deep=False, objs=[map, *map.items, *players],
                                              uid='Whole Game', rollback_len=5)
        # init others
        self.__register_event_handler()

    def __register_event_handler(self)->None:
        ev.event_to_game_rollback.connect(self.event_to_game_rollback)
    
    def __unregister_event_handler(self)->None:
        ev.event_to_game_rollback.disconnect(self.event_to_game_rollback)

    def event_to_game_rollback(self, sender: Any, rounds: int)->None:
        '''rollback the whole game

        :param sender: Any, not used
        :param rounds: rounds to rollback
        '''
        self.__transaction.rollback(step=rounds)
        raise util.RollbackException('%s rollback exception...' % self.__transaction.uid)

    @property
    def map(self)->itf.IGameForMap:
        return self.__map

    def run(self):
        '''run the game and show results of each step
        '''
        while True:
            try:
                if not self.map.run_one_round():
                    break
            except util.RollbackException as err:
                logging.warning(str(err))
            else:
                self.__transaction.commit()
        self.destroy()

    def destroy(self):
        self.map.destroy()
        if self.display_frame:
            self.display_frame.destroy()
        self.__unregister_event_handler()

class Game(BaseGame):
    pass