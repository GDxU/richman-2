# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

import richman.event as ev
from richman.player import BasePlayer, PlayerSimple
import richman.utility as util
import richman.interface as itf


class TestBasePlayer(unittest.TestCase):

    def setUp(self):
        map = MagicMock()
        map.__len__.return_value = 10
        self.player = BasePlayer(name='dengzhe', money=10000)
        self.player.add_map(map)

    def tearDown(self):
        pass

    def test_add_money_should_execute_correctlly(self):
        ev.event_to_player_add_money.send(None, player=self.player,
                                          money_delta=-10000)
        self.player._make_money = MagicMock()
        ev.event_to_player_add_money.send(None, player=self.player,
                                          money_delta=-1)
        self.assertTrue(self.player._make_money.called)

    def test_pos_should_set_right_value(self):
        pos_max = len(self.player.map)
        ev.event_to_player_move_to.send(None, player=self.player,
                                        pos=pos_max+3)
        self.assertEqual(self.player.pos, 3)

    def test_pos_queue_should_push_and_pull_with_delay_correctly(self):
        self.player._push_pos(pos=10, delay_turns=2)
        self.assertIsNone(self.player._pull_pos())
        self.assertEqual(self.player._pull_pos(), 10)
        self.player._push_pos(pos=10, delay_turns=1)
        self.player._push_pos(pos=10, delay_turns=1)
        with self.assertRaises(AssertionError):
            self.player._pull_pos()


class TestPlayerSimple(unittest.TestCase):

    def setUp(self):
        map = MagicMock()
        map.__len__.return_value = 10
        self.player = PlayerSimple(name='dengzhe', money=10000)
        self.player.add_map(map)
        estate1 = MagicMock(spec=itf.IPlayerForEstate)
        estate1.name = 'e1'
        estate1.buy_value = 10
        estate1.owner = None
        estate1.pos_in_map = 0
        BasePlayer._BasePlayer__event_handler_buy_decision(estate1, self.player)
    
    def tearDown(self):
        pass

    def test_player_should_rollback_correctly(self):
        self.assertEqual(self.player.estates[0].name, 'e1')
        mementos = util.Transaction(False, self.player, 5, 'player memento')
        estate2 = MagicMock(spec=itf.IPlayerForEstate)
        estate2.name = 'e2'
        estate2.buy_value = 10
        estate2.owner = None
        estate2.pos_in_map = 1
        BasePlayer._BasePlayer__event_handler_buy_decision(estate2, self.player)
        mementos.commit()
        estate3 = MagicMock(spec=itf.IPlayerForEstate)
        estate3.name = 'e3'
        estate3.buy_value = 10
        estate3.owner = None
        estate3.pos_in_map = 2
        BasePlayer._BasePlayer__event_handler_buy_decision(estate3, self.player)
        mementos.commit()
        self.assertEqual(len(mementos), 3)
        self.assertListEqual([estate.name for estate in self.player.estates], ['e1', 'e2', 'e3'])
        # roll back
        mementos.rollback(step=3)
        self.assertEqual(len(mementos), 0)
        self.assertListEqual([estate.name for estate in self.player.estates], ['e1'])
