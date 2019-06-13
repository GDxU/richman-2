# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.map import MapImplement
from richman.base import BasePlace


class TestBaseMap(unittest.TestCase):

    def setUp(self):
        place1 = MagicMock()
        place2 = MagicMock()
        place3 = MagicMock()
        self.map = MapImplement('China', [place1, place2, place3])

    def tearDown(self):
        pass

    def test_add_to_map_should_add_places_and_players_to_map(self):
        place1 = MagicMock()
        place2 = MagicMock()
        map = MapImplement('China', [place1, place2])
        self.assertListEqual(
            map.items,
            [place1,
             place2]
        )

    def test_save_and_load_map_should_operate_correctly(self):
        self.map.save(r'./map_test.pickle')
        map_new = MapImplement(name='China New')
        map_new.load(r'./map_test.pickle')
        self.assertEqual(self.map.name, map_new.name)
        self.assertEqual(map_new.items[0].name, 'Hangzhou')
        self.assertEqual(map_new.items[1].name, 'Xiamen')
        self.assertEqual(map_new.items[2].name, 'Shanxi')
