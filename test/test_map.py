# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.map import (
    BaseMap,
    PlaceAlreadyExistInMapException,
    PlayerAlreadyExistException
)
from richman.place import BasePlace, PlaceEstate, PlaceEstateBlock


class TestBaseMap(unittest.TestCase):

    def setUp(self):
        place1 = BasePlace('Hangzhou', 2200, 1100)
        place2 = BasePlace('Xiamen', 3300, 2200)
        place3 = BasePlace('Shanxi', 4400, 2200)
        self.map = BaseMap('China', [place1, place2, place3])

    def tearDown(self):
        pass

    def test_add_to_map_should_add_places_and_players_to_map(self):
        block = PlaceEstateBlock('block1')
        place1 = PlaceEstate('Hangzhou', [1,2,3,4], 2200, 1100, 1, block)
        place2 = PlaceEstate('Xiamen', [1,2,3,4], 3300, 2200, 2, block)
        place3 = PlaceEstate('Xiamen', [1,2,3,4], 4400, 2200, 3, block)
        with self.assertRaises(PlaceAlreadyExistInMapException):
            map = BaseMap('China', [place1, place2, place3])
        map = BaseMap('China', [place1, place2])
        self.assertListEqual(
            map.items,
            [place1,
             place2]
        )

    def test_save_and_load_map_should_operate_correctly(self):
        self.map.save(r'./map_test.pickle')
        map_new = BaseMap(name='China New')
        map_new.load(r'./map_test.pickle')
        self.assertEqual(self.map.name, map_new.name)
        self.assertEqual(map_new.items[0].name, 'Hangzhou')
        self.assertEqual(map_new.items[1].name, 'Xiamen')
        self.assertEqual(map_new.items[2].name, 'Shanxi')
