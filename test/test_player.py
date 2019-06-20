# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

import richman.event as ev
from richman.player import BasePlayer


class TestBasePlayer(unittest.TestCase):

    def setUp(self):
        map = MagicMock()
        map.__len__.return_value = 10
        self.player = BasePlayer(name='Hangzhou', money=10000)
        self.player.add_map(map)

    def tearDown(self):
        pass

    def test_add_money_should_execute_correctlly(self):
        ev.event_to_player_add_money.send(None, receiver=self.player,
                                          money_delta=-10000)
        self.player._make_money = MagicMock()
        ev.event_to_player_add_money.send(None, receiver=self.player,
                                          money_delta=-1)
        self.assertTrue(self.player._make_money.called)

    def test_pos_should_set_right_value(self):
        pos_max = len(self.player.map)
        ev.event_to_player_move_to.send(None, receiver=self.player,
                                        pos=pos_max+3)
        self.assertEqual(self.player.pos, 3)


class TestPlayerSimple(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass