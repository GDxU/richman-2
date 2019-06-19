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


# player interface

class IPlayerBase(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        pass

class IPlayerForMap(IPlayerBase):

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
    def map(self):
        pass
    @map.setter
    @abc.abstractmethod
    def map(self, value):
        '''set player's map

        :param value: map
        '''
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
    def dice(self)->int:
        '''dice

        :return: current pos of player 
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, obj):
        pass

class IMapForEPlace(abc.ABC):

    @abc.abstractmethod
    def __eq__(self, obj):
        pass

class IMapForEstate(IMapForEPlace):

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
