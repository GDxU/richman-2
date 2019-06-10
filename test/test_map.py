# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.map import (
    BaseMap,
    PlaceAlreadyExistException,
    PlayerAlreadyExistException
)
from richman.place import BasePlace


class TestBaseMap(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_add_to_map_should_add_places_and_players_to_map(self):
        place1 = BasePlace('Hangzhou', 2200, 1100)
        place2 = BasePlace('Xiamen', 3300, 2200)
        place3 = BasePlace('Xiamen', 4400, 2200)
        with self.assertRaises(PlaceAlreadyExistException):
            map = BaseMap('China', [place1, place2, place3])
        map = BaseMap('China', [place1, place2])
        self.assertListEqual(
            map.places,
            [place1,
             place2]
        )

