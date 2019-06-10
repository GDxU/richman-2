# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


from richman.place import (
    BasePlace,
    PledgeWithNoOwnerException,
    PledgeTwiceException,
    BuyPlaceWithoutEnoughMoneyException
)
from richman.player import BasePlayer


class TestBasePlace(unittest.TestCase):

    def setUp(self):
        self.hangzhou = BasePlace('Hangzhou', 2200, 1100)
    
    def tearDown(self):
        pass

    def test_base_place_init_should_set_vars_properly(self):
        self.assertEqual(self.hangzhou.name, 'Hangzhou')
        self.assertEqual(self.hangzhou.buy_value, 2200)
        self.assertEqual(self.hangzhou.pledge_value, 1100)

    def test_base_place_pledge_should_execute_correctlly(self):
        with self.assertRaises(PledgeWithNoOwnerException):
            self.hangzhou.pledge()
        player = BasePlayer('Dengzhe', 10000)
        self.hangzhou.buy(player)
        self.hangzhou.pledge()
        with self.assertRaises(PledgeTwiceException):
            self.hangzhou.pledge()

    def test_buy_should_fail_for_not_enough_money(self):
        with self.assertRaises(BuyPlaceWithoutEnoughMoneyException):
            player = BasePlayer('Dengzhe', 1000)
            self.hangzhou.buy(player)

    def test_two_place_eq_check(self):
        place1 = BasePlace('Hangzhou', 2200, 1100)
        place2 = BasePlace('Xiamen', 3300, 1100)
        self.assertEqual(self.hangzhou, place1)
        self.assertNotEqual(self.hangzhou, place2)


class TestPlaceEstate(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

