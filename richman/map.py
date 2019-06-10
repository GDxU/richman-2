# -*- coding: utf-8 -*
'''map
'''
from richman.place import BasePlace
from richman.player import BasePlayer


class PlaceAlreadyExistException(Exception):
    def __init__(self, *args):
        super().__init__("该土地或项目已经存在！")

class PlayerAlreadyExistException(Exception):
    def __init__(self, *args):
        super().__init__("该玩家已经存在！")


class BaseMap:

    __places = []
    __places_set = set()
    
    def __init__(self, name: str, places: list):
        '''init

        :param name: map name
        :param places: places in the map
        '''
        self.__name = name
        self.__places = []
        self.__places_set = set()
        self._add_places_to_map(places)

    @property
    def name(self):
        return self.__name
    @property
    def places(self):
        return self.__places

    def _add_places_to_map(self, places: list):
        if places and not isinstance(places, list):
            places = [places]
        for place in places:
            if not place.name in self.__places_set:
                self.__places.append(place)
                self.__places_set.add(place.name)
            else:
                raise PlaceAlreadyExistException()