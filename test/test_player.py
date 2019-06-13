# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


from richman.player import PlayerImplement
# from richman.maps.map_test import MapTest


class TestBasePlayer(unittest.TestCase):

    def setUp(self):
        # map = MapTest()
        map = MagicMock()
        map.__len__.return_value = 10
        self.player = PlayerImplement(name='Hangzhou',
                                      money=10000,
                                      map=map)
    
    def tearDown(self):
        pass

    def test_add_money_should_execute_correctlly(self):
        self.player.add_money(-10000)
        self.player._make_money = MagicMock()
        self.player.add_money(-1)
        self.assertTrue(self.player._make_money.called)

    def test_pos_should_set_right_value(self):
        pos_max = len(self.player.map)
        self.player.pos = pos_max + 3
        self.assertEqual(self.player.pos, 3)


class TestPlayerSimple(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass