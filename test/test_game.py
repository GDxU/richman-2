# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.place import BasePlace
from richman.map import BaseMap
from richman.player import BasePlayer
from richman.game import BaseGame, PlayerNamesDuplicatedException


class TestBaseGame(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_build_players_should_build_players_with_right_params(self):
        game = BaseGame(None, ['戎萍', '邓哲', '邓彦修'], 20000)

        self.assertEqual(len(game.players), 3)

        self.assertEqual(game.players[0].name, '戎萍')
        self.assertEqual(game.players[0].money, 20000)

        self.assertEqual(game.players[1].name, '邓哲')
        self.assertEqual(game.players[1].money, 20000)

        self.assertEqual(game.players[2].name, '邓彦修')
        self.assertEqual(game.players[2].money, 20000)

        with self.assertRaises(PlayerNamesDuplicatedException):
            game = BaseGame(None, ['戎萍', '戎萍'], 20000)

    # def test_
