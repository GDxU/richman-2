# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.game import Game


class TestBaseGame(unittest.TestCase):

    def setUp(self):
        self.map = MagicMock()
        self.map.add_players = MagicMock()
        self.game = Game(self.map, None)

    def tearDown(self):
        pass

    def test_run_should_finish_when_only_one_player_is_left(self):
        self.map.run_one_round = MagicMock()
        self.map.run_one_round.side_effect = [True, True, False]
        self.game.run()
        self.assertEqual(self.map.run_one_round.call_count, 3)
