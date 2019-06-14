# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.game import Game
from richman.maps.map_test import MapTest
from richman.player import PlayerSimple


class TestRichMan(unittest.TestCase):

    def setUp(self):
        # player
        init_money = 20000
        player1 = PlayerSimple(name='邓哲', money=init_money)
        player2 = PlayerSimple(name='戎萍', money=init_money)
        # map
        map = MapTest()
        # game
        self.game = Game(map, [player1, player2])

    def tearDown(self):
        pass

    def test_all_players_should_be_banckrupted_at_last(self):
        self.game.run()
        self.assertEqual(len(self.game.players_in_game), 1)


if __name__ == "__main__":
    unittest.main()