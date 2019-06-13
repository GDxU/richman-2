# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

from richman.game import GameImplement


class TestBaseGame(unittest.TestCase):

    def setUp(self):
        map = MagicMock()
        self.player1 = MagicMock()
        self.player1.name = '邓哲'
        self.player1.is_banckrupted = False
        self.player1.play = MagicMock()
        self.player2 = MagicMock()
        self.player2.name = '戎萍'
        self.player2.is_banckrupted = False
        self.player2.play = MagicMock()
        players = [self.player1, self.player2]
        self.game = GameImplement(map, players)

    def tearDown(self):
        pass

    def test_run_should_finish_when_all_players_banckrupted(self):
        self.game._run_one_step()
        self.player1.play.assert_called_once()
        self.player2.play.assert_called_once()

        self.player1.is_banckrupted = True
        self.game._run_one_step()
        self.assertEqual(len(self.game.players), 1)
        self.assertEqual(self.game.players[0].name, '戎萍')
        
        self.player2.is_banckrupted = True
        self.game._run_one_step()
        self.assertFalse(self.game.players)