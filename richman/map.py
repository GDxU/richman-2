# -*- coding: utf-8 -*
'''map
'''
import pickle
import os

import richman.interface as itf


class PlayerAlreadyExistException(Exception):
    def __init__(self, *args):
        super().__init__("该玩家已经存在！")


class MapImplement(itf.IPlayerForMap):

    __items = []
    _blocks = []

    def __init__(self, name: str, items:list = None):
        '''init

        :param name: map name
        :param items: items in the map
        '''
        self.__name = name
        self.__items = []
        self._blocks = []
        if items:
            self._add_items(items)

    @property
    def name(self):
        return self.__name
    @property
    def items(self):
        return self.__items
    @property
    def blocks(self):
        return self._blocks

    def _add_items(self, items: list):
        if items and not isinstance(items, list):
            items = [items]
        self.__items.extend(items)

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

    def trigger(self, player: itf.IMapForPlayer):
        '''trigger player to 
        '''
        self.items[player.pos].trigger(player)

    def __len__(self):
        return len(self.items)
