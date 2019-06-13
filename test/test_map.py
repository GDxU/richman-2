# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.map import MapImplement


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
