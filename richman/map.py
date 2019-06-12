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
    __blocks = []
    __estate_set = set()
    
    def __init__(self, name: str, items:list = None):
        '''init

        :param name: map name
        :param items: items in the map
        '''
        self.__name = name
        self.__items = []
        self.__blocks = []
        self.__estate_set = set()
        if items:
            self._add_items(items)

    @property
    def name(self):
        return self.__name
    @property
    def items(self):
        return self.__items

    def _add_items(self, items: list):
        if items and not isinstance(items, list):
            items = [items]
        for item in items:
            if isinstance(item, PlaceEstate):
                if not item.name in self.__estate_set:
                    self.__items.append(item)
                    self.__estate_set.add(item.name)
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

    def __len__(self):
        return len(self.items)
