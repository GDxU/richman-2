# -*- coding: utf-8 -*
'''map
'''
import pickle
import os

from richman.place import BasePlace
from richman.player import BasePlayer


class PlaceAlreadyExistInMapException(Exception):
    def __init__(self, *args):
        super().__init__("该土地或项目已经存在！")

class PlayerAlreadyExistException(Exception):
    def __init__(self, *args):
        super().__init__("该玩家已经存在！")


class BaseMap:

    __items = []
    __items_set = set()
    
    def __init__(self, name: str, items:list = []):
        '''init

        :param name: map name
        :param items: items in the map
        '''
        self.__name = name
        self.__items = []
        self.__items_set = set()
        self._add_items_to_map(items)

    @property
    def name(self):
        return self.__name
    @property
    def items(self):
        return self.__items

    def _add_items_to_map(self, items: list):
        if items and not isinstance(items, list):
            items = [items]
        for item in items:
            if isinstance(item, PlaceEstate):
                if not item.name in self.__items_set:
                    self.__items.append(item)
                    self.__items_set.add(item.name)
                else:
                    raise PlaceAlreadyExistInMapException()
            else:
                self.__items.append(item)

    def load(self, file_path: str):
        '''load map from pickle

        :param file_path: file_path to load
        '''
        assert os.path.exists(file_path),\
            '用于读取 map 的文件不存在：{}。'.format(file_path)
        with open(file_path, 'rb') as f:
            map = pickle.load(f)
        assert map, '读取或解析失败：{}。'
        self.__items = map['items']
        self.__name = map['name']

    def save(self, file_path: str):
        '''save map into pickle

        :param file_path: file_path to save
        '''
        map = {}
        map['items'] = self.items
        map['name'] = self.name
        with open(file_path, 'wb') as f:
            pickle.dump(map, f)


from richman.place import (
    PlaceEstate,
    PlaceEstateBlock,
    PlaceProjectNuclear,
    PlaceProjectBuilder,
    PlaceProjectStation,
    PlaceProjectTv,
    PlaceProjectAirport,
    PlaceProjectSewerage,
    PlaceProjectSeaport
)
from richman.event import (
    EventStart,
    EventNews,
    EventTrial,
    EventLuck,
    EventStock,
    EventPrison,
    EventPark,
    EventTax
)

class MapSuperRichman(BaseMap):
    '''超级地产富翁：地产大亨
    '''
    __blocks = []
    __estates = []

    def __init__(self):
        self.__name == '超级地产富翁：地产大亨'
        self._build()
    
    @property
    def name(self):
        return self.__name

    def _build(self):
        # setup estate block
        self.__blocks = []
        self.__blocks.append(PlaceEstateBlock('block0'))
        self.__blocks.append(PlaceEstateBlock('block1'))
        self.__blocks.append(PlaceEstateBlock('block2'))
        self.__blocks.append(PlaceEstateBlock('block3'))
        self.__blocks.append(PlaceEstateBlock('block4'))
        self.__blocks.append(PlaceEstateBlock('block5'))
        # setup estates
        self.__estates = []
        self.__estates.append(PlaceEstate(
            name='沈阳',
            fees=[400, 1000, 2500, 5500],
            buy_value=2400,
            pledge_value=1200,
            upgrade_value=600,
            block=self.__blocks[0]
            ))
        self.__estates.append(PlaceEstate(
            name='天津',
            fees=[500, 1100, 3000, 6000],
            buy_value=2600,
            pledge_value=1300,
            upgrade_value=600,
            block=self.__blocks[0]
            ))