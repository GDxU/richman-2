# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.map import BaseMap
import richman.interface as itf


class TestBaseMap(unittest.TestCase):

    def setUp(self):
        estate1 = MagicMock(spec=itf.IMapForEstate)
        estate1.name = 'p1'
        estate2 = MagicMock(spec=itf.IMapForEstate)
        estate2.name = 'p2'
        estate3 = MagicMock(spec=itf.IMapForEstate)
        estate3.name = 'p3'
        self.map = BaseMap('China', [estate1, estate2, estate3])

    def tearDown(self):
        pass

    def test_add_to_map_should_add_estates_and_players_to_map(self):
        estate1 = MagicMock(spec=itf.IMapForEstate)
        estate1.name = 'p1'
        estate2 = MagicMock(spec=itf.IMapForEstate)
        estate2.name = 'p2'
        estate3 = MagicMock(spec=itf.IMapForEstate)
        estate3.name = 'p2'
        # init correctly
        map = BaseMap('China', [estate1, estate2])
        self.assertListEqual(
            map.items,
            [estate1,
             estate2]
        )
        # init with duplicated estates
        with self.assertRaises(ValueError):
            map = BaseMap('China', [estate1, estate2, estate3])
