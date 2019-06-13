# -*- coding: utf-8 -*
'''接口类
'''
import abc


class IGamePlayer(abc.ABC):
    '''player of game interface
    '''

    @property
    @abc.abstractmethod
    def name(self)->str:
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


class IPlayerMap(abc.ABC):
    '''map of player interface
    '''

    @abc.abstractmethod
    def trigger(self, player):
        '''trigger player to 
        '''
        pass

    @abc.abstractmethod
    def __len__(self):
        '''
        :return: length of map
        '''
        pass


class IPlayerPlace(abc.ABC):
    '''player interface to place
    '''

    @property
    @abc.abstractmethod
    def is_pledged(self):
        pass
    @property
    @abc.abstractmethod
    def buy_value(self):
        pass
    @property
    @abc.abstractmethod
    def pledge_value(self):
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
    def sell(self):
        '''sell the place, remove the owner mark of the place
        '''
        pass

    @abc.abstractmethod
    def rebuy(self):
        '''re-buy the place when it is pledged
        '''
        pass

    @abc.abstractmethod
    def trigger(self, player):
        '''take the effect of the place, triggered by the player

        :param player: BasePlayer
        '''
        pass

    @abc.abstractmethod
    def __str__(self):
        '''display player info
        '''
        pass


class IPlayerEvent(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def trigger(self, player):
        '''take the effect of the place, triggered by the player
        '''
        pass


class IMapPlayer(abc.ABC):
    @property
    @abc.abstractmethod
    def map(self):
        pass
    @map.setter
    @abc.abstractmethod
    def map(self, value: IPlayerMap):
        pass
    @property
    @abc.abstractmethod
    def pos(self):
        pass


class IPlacePlayer(abc.ABC):
    '''place interface to player
    '''

    @abc.abstractmethod
    def add_money(self, delta: int):
        '''change player money

        :param delta: minus means subtract
        '''
        pass

    @abc.abstractmethod
    def trigger_buy(self, place):
        '''decide whether to buy the place

        :param place: IPlayerPlace
        '''
        pass

    @abc.abstractmethod
    def trigger_upgrade(self, place):
        '''decide whether to upgrade the place

        :param place: IPlayerPlace
        '''
        pass

    @abc.abstractmethod
    def trigger_jump_to_estate(self):
        '''select which estate to go when jump is needed
        '''
        pass

    @abc.abstractmethod
    def move_to(self, pos: int):
        '''move player to pos

        :param pos: position to move to
        '''
        pass

    @abc.abstractmethod
    def __eq__(self, obj):
        '''check if two player equls
        '''
        pass
