# -*- coding: utf-8 -*
'''事件类
'''
import richman.interface as itf


class BaseEvent(itf.IEventManagerForEvent):

    def __init__(self, name: str):
        '''init
        
        :param name: name of event, str
        '''
        self.__name = name

    @property
    def name(self):
        return self.__name

    def _build_name(self, id)->str:
        '''build the event name with the id

        :param id: the id to build the name
        :return: event name with id
        '''
        class_name = self.__class__.__name__
        return '%s_%s' % (class_name, id)


# event to player

class EventToPlayerAddMoney(BaseEvent):

    def __init__(self, player_name: str, delta: int):
        event_name = self._build_name(player_name)
        super().__init__(name=event_name)
        self.__delta = delta

    @property
    def delta(self):
        return self.__delta


class EventToPlayerMoveTo(BaseEvent):

    def __init__(self, player_name: str, pos: int):
        event_name = self._build_name(player_name)
        super().__init__(name=event_name)
        self.__pos = pos

    @property
    def pos(self):
        return self.__pos


class EventToPlayerBuyPlace(BaseEvent):

    def __init__(self, player_name: str, place: itf.IPlayerForPlace):
        event_name = self._build_name(player_name)
        super().__init__(name=event_name)
        self.__place = place

    @property
    def place(self):
        return self.__place


class EventToPlayerUpgradeEstate(BaseEvent):

    def __init__(self, player_name: str, estate: itf.IPlayerForEstate):
        event_name = self._build_name(player_name)
        super().__init__(name=event_name)
        self.__estate = estate

    @property
    def estate(self):
        return self.__estate


class EventToPlayerJumpToEstate(BaseEvent):

    def __init__(self, player_name: str):
        event_name = self._build_name(player_name)
        super().__init__(name=event_name)


class EventToPlayerUpgradeAnyEstate(BaseEvent):

    def __init__(self, player_name: str):
        event_name = self._build_name(player_name)
        super().__init__(name=event_name)


# event to place

class EventToPlaceBuy(BaseEvent):

    def __init__(self, place_name: str, player: itf.IPlayerForPlace):
        event_name = self._build_name(place_name)
        super().__init__(name=event_name)
        self.__player = player

    @property
    def player(self):
        return self.__player


class EventToPlaceSell(BaseEvent):

    def __init__(self, place_name: str, player):
        event_name = self._build_name(place_name)
        super().__init__(name=event_name)
        self.__player = player

    @property
    def player(self):
        return self.__player


# event to estate

class EventToEstateUpgrade(BaseEvent):

    def __init__(self, estate_name: str, player):
        event_name = self._build_name(estate_name)
        super().__init__(name=event_name)
        self.__player = player

    @property
    def player(self):
        return self.__player


# event to project
