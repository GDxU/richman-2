# -*- coding: utf-8 -*
'''接口类
'''
import abc


# game interface

class IGameForPlayer(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        '''
        :return: name of the player
        '''
        pass
    @property
    @abc.abstractmethod
    def is_banckrupted(self)->bool:
        '''
        :return: True if is banckrupted.
        '''
        pass

    @abc.abstractmethod
    def __str__(self):
        '''display player info
        '''
        pass

class IGameForMap(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        '''
        :return: name of the player
        '''
        pass

    @abc.abstractmethod
    def add_players(self, players: list):
        '''add players to map

        :param players: list of players
        '''
        pass

    @abc.abstractmethod
    def run_one_round(self)->bool:
        '''run one round of the map, which means every player run once

        :return: False if only one player is left
        '''
        pass


# player interface

class IPlayerBase(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        pass

class IPlayerForMap(IPlayerBase):

    @property
    def items(self)->list:
        pass
    @property
    @abc.abstractmethod
    def players_in_game(self):
        pass

    @abc.abstractmethod
    def __len__(self):
        '''
        :return: length of map
        '''
        pass

class IPlayerForPlace(IPlayerBase):

    @property
    @abc.abstractmethod
    def is_available(self):
        '''是否可以购买'''
        pass
    @property
    @abc.abstractmethod
    def buy_value(self):
        pass
    @property
    @abc.abstractmethod
    def sell_value(self):
        pass

    @abc.abstractmethod
    def __str__(self):
        '''display place info
        '''
        pass

class IPlayerForEstate(IPlayerForPlace):

    @property
    @abc.abstractmethod
    def upgrade_value(self):
        pass
    @property
    @abc.abstractmethod
    def is_pledged(self):
        pass
    @property
    @abc.abstractmethod
    def pledge_value(self):
        pass
    @property
    @abc.abstractmethod
    def is_level_max(self):
        pass
    @property
    @abc.abstractmethod
    def current_level(self):
        pass
    @property
    @abc.abstractmethod
    def fees(self):
        '''所有的过路费用'''
        pass

class IPlayerForProject(IPlayerForPlace):

    pass


# map interface

class IMapForPlayer(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self)->str:
        pass
    @property
    @abc.abstractmethod
    def map(self):
        pass
    @property
    @abc.abstractmethod
    def pos(self):
        pass
    @property
    @abc.abstractmethod
    def is_banckrupted(self)->bool:
        '''
        :return: True if is banckrupted.
        '''
        pass

    @abc.abstractmethod
    def add_map(self, map)->None:
        '''add map to player

        :param map: map with IPlayerForMap interface
        '''
        pass

    @abc.abstractmethod
    def dice(self)->int:
        '''dice

        :return: current pos of player 
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, obj):
        pass

class IMapForItem(abc.ABC):

    @abc.abstractmethod
    def trigger(self, player):
        '''trigger the effect of the item in the map

        :param player: the player that trigger the effect
        '''
        pass

class IMapForPlace(IMapForItem):

    @abc.abstractmethod
    def __eq__(self, obj):
        pass

class IMapForEstate(IMapForPlace):

    pass

class IMapForProject(IMapForPlace):

    pass

class IMapForPublic(IMapForItem):

    pass


# place interface

class IPlaceForPlayer(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        '''
        :return: name of the player
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, obj):
        '''check if two player equls
        '''
        pass

# estate interface

class IEstateForPlayer(IPlaceForPlayer):
    
    pass


# project interface

class IProjectForPlayer(IPlaceForPlayer):

    @property
    @abc.abstractmethod
    def estate_max_level(self):
        '''return the max level of all the estate the player has
        '''
        pass
