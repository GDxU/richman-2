# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


from dafuweng.player import (
    BasePlayer,
    PlayerMoneyBelowZeroException
)


class TestBasePlayer(unittest.TestCase):

    def setUp(self):
        self.dengzhe = BasePlayer('Hangzhou', 10000)
    
    def tearDown(self):
        pass

    def test_add_money_should_execute_correctlly(self):
        self.dengzhe.add_money(-10000)
        with self.assertRaises(PlayerMoneyBelowZeroException):
            self.dengzhe.add_money(-1)
    
    def test_pos_should_set_right_value(self):
        self.dengzhe.pos_max = 10
        self.dengzhe.pos = 13
        self.assertEqual(self.dengzhe.pos, 3)

