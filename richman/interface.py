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

    @abc.abstractmethod
    def trigger(self, player):
        '''trigger player to 
        '''
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
    def buy_value(self):
        pass
    @property
    @abc.abstractmethod
    def sell_value(self):
        pass

    @abc.abstractmethod
    def buy(self, player):
        '''player buy the place

        :param player: the player to buy the place
        '''
        pass

    @abc.abstractmethod
    def sell(self):
        '''sell the place, remove the owner mark of the place
        '''
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
    def is_available(self):
        pass
    @property
    @abc.abstractmethod
    def is_level_max(self):
        pass
    @property
    @abc.abstractmethod
    def current_level(self):
        pass

    @abc.abstractmethod
    def upgrade(self):
        '''upgrade the place
        '''
        pass

    @abc.abstractmethod
    def pledge(self):
        '''pledge the place to the bank
        '''
        pass

    @abc.abstractmethod
    def rebuy(self):
        '''re-buy the place when it is pledged
        '''
        pass


class IPlayerForProject(IPlayerForPlace):

    pass


class IPlayerForEvent(IPlayerBase):

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


# estate interface

class IEstateForPlayer(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        '''
        :return: name of the player
        '''
        pass

    @abc.abstractmethod
    def add_money(self, delta: int):
        '''change player money

        :param delta: minus means subtract
        '''
        pass

    @abc.abstractmethod
    def trigger_buy(self, place):
        '''decide whether to buy the place

        :param place: IPlayerForPlace
        '''
        pass

    @abc.abstractmethod
    def trigger_upgrade(self, place):
        '''decide whether to upgrade the place

        :param place: IPlayerForPlace
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, obj):
        pass


# project interface

class IProjectForPlayer(abc.ABC):

    @property
    @abc.abstractmethod
    def estate_max_level(self):
        '''return the max level of all the estate the player has
        '''
        pass

    @abc.abstractmethod
    def add_money(self, delta: int):
        '''change player money

        :param delta: minus means subtract
        '''
        pass

    @abc.abstractmethod
    def trigger_buy(self, place):
        '''decide whether to buy the place

        :param place: IPlayerForPlace
        '''
        pass

    @abc.abstractmethod
    def trigger_jump_to_estate(self):
        '''select which estate to go when jump is needed
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, obj):
        '''check if two player equls
        '''
        pass
