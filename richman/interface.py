# -*- coding: utf-8 -*
'''接口类
'''
import abc


# event manager

class IEventManagerForEvent(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        '''
        :return: name of the event
        '''
        pass

class IForEventManager(abc.ABC):

    @abc.abstractmethod
    def add_listeners(self, name: str, handlers: list):
        '''add handler to the name list

        :param name: type of event, str
        :param handlers: handlers to process the event
        '''
        pass

    @abc.abstractmethod
    def remove_listeners(self, name: str, handlers: list):
        '''remove handler from the name list

        :param name: type of event, str
        :param handlers: handlers to process the event
        '''
        pass

    @abc.abstractmethod
    def send(self, event: IEventManagerForEvent):
        '''send the event to handlers

        :param event: the event to send
        '''
        pass


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
    def add_to_map(self, map):
        '''add player to map

        :param map: map
        '''
        pass

    @abc.abstractmethod
    def play(self):
        '''play the game, like dice etc.
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
    def pos(self):
        pass

class IMapForEstate(abc.ABC):

    @abc.abstractmethod
    def __eq__(self, obj):
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
