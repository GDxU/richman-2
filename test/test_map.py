# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.map import BaseMap
import richman.interface as itf


class TestBaseMap(unittest.TestCase):

    def setUp(self):
        estate1 = MagicMock(spec=itf.IMapForEstate)
        estate1.name = 'p1'
        estate1.trigger = MagicMock()
        estate2 = MagicMock(spec=itf.IMapForEstate)
        estate2.name = 'p2'
        estate2.trigger = MagicMock()
        estate3 = MagicMock(spec=itf.IMapForEstate)
        estate3.name = 'p3'
        estate3.trigger = MagicMock()
        self.player1 = MagicMock()
        self.player1.name = '邓哲'
        self.player1.is_banckrupted = False
        self.player1.take_the_turn = MagicMock()
        self.player2 = MagicMock()
        self.player2.name = '戎萍'
        self.player2.is_banckrupted = False
        self.player2.take_the_turn = MagicMock()
        players = [self.player1, self.player2]
        self.map = BaseMap('China')
        self.map.add_items([estate1, estate2, estate3])
        self.map.add_players(players)

    def tearDown(self):
        pass

    def test_add_to_map_should_add_estates_and_players_to_map(self):
        estate1 = MagicMock(spec=itf.IMapForEstate)
        estate1.name = 'p1'
        estate1.trigger = MagicMock()
        estate2 = MagicMock(spec=itf.IMapForEstate)
        estate2.name = 'p2'
        estate2.trigger = MagicMock()
        estate3 = MagicMock(spec=itf.IMapForEstate)
        estate3.name = 'p3'
        estate3.trigger = MagicMock()
        # init correctly
        map = BaseMap('China')
        map.add_items([estate1, estate2, estate3])
        self.assertListEqual(
            map.items,
            [estate1,
             estate2,
             estate3]
        )
        # add items with duplicated estates
        with self.assertRaises(AssertionError):
            map.add_items(estate1)

    def test_run_one_round_should_finish_when_all_players_banckrupted(self):
        self.assertTrue(self.map.run_one_round())
        self.player1.take_the_turn.assert_called_once()
        self.player2.take_the_turn.assert_called_once()

        self.player1.is_banckrupted = True
        self.assertFalse(self.map.run_one_round())
        self.assertEqual(len(self.map.players_in_game), 1)
        self.assertEqual(self.map.players_in_game[0].name, '戎萍')
