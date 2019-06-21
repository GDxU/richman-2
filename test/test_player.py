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

    def test_pos_queue_should_push_and_pull_with_delay_correctly(self):
        self.player._push_pos(pos=10, delay=2)
        self.assertIsNone(self.player._pull_pos())
        self.assertEqual(self.player._pull_pos(), 10)
        self.player._push_pos(pos=10, delay=1)
        self.player._push_pos(pos=10, delay=1)
        with self.assertRaises(AssertionError):
            self.player._pull_pos()


class TestPlayerSimple(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass