# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


from richman.place import (
    BasePlace,
    PlaceEstate,
    PlaceEstateBlock,
    PledgeWithNoOwnerException,
    PledgeTwiceException,
    RebuyNotPledgedException
)
from richman.player import (BasePlayer, PlayerMoneyBelowZeroException) 


class TestBasePlace(unittest.TestCase):

    def setUp(self):
        self.hangzhou = BasePlace('Hangzhou', 2200, 1100)
    
    def tearDown(self):
        pass

    def test_base_place_init_should_set_vars_properly(self):
        self.assertEqual(self.hangzhou.name, 'Hangzhou')
        self.assertEqual(self.hangzhou.buy_value, 2200)
        self.assertEqual(self.hangzhou.pledge_value, 1100)

    def test_buy_and_rebuy_should_raise_execption(self):
        player = BasePlayer('Dengzhe', 100)
        with self.assertRaises(PlayerMoneyBelowZeroException):
            self.hangzhou.buy(player)
        player.money = 10000
        self.hangzhou.buy(player)
        with self.assertRaises(RebuyNotPledgedException):
            self.hangzhou.rebuy()
        self.hangzhou.pledge()
        player.money = 10
        with self.assertRaises(PlayerMoneyBelowZeroException):
            self.hangzhou.rebuy()

    def test_base_place_pledge_should_execute_correctlly(self):
        with self.assertRaises(PledgeWithNoOwnerException):
            self.hangzhou.pledge()
        player = BasePlayer('Dengzhe', 10000)
        self.hangzhou.buy(player)
        self.hangzhou.pledge()
        with self.assertRaises(PledgeTwiceException):
            self.hangzhou.pledge()

    def test_two_place_eq_check(self):
        place1 = BasePlace('Hangzhou', 2200, 1100)
        place2 = BasePlace('Xiamen', 3300, 1100)
        self.assertEqual(self.hangzhou, place1)
        self.assertNotEqual(self.hangzhou, place2)


class TestPlaceEstate(unittest.TestCase):
    
    def setUp(self):
        self.block = PlaceEstateBlock('block1')
        self.fees = [100, 200, 300, 400]
        self.estate = PlaceEstate('杭州', self.fees,
                                  2000, 1000, 300, self.block)
        self.player = BasePlayer('邓哲', 10000)

    def tearDown(self):
        pass

    def test_fees_should_go_up_with_level_up(self):
        fees = [100, 20, 300, 400]
        with self.assertRaises(AssertionError):
            PlaceEstate('杭州', fees,
                         2000, 1000, 300, self.block)

    def test_upgrade_should_run_correctly_and_raise_exception(self):
        self.player.money = 10000
        self.estate.buy(self.player)
        self.player.money = 10
        with self.assertRaises(PlayerMoneyBelowZeroException):
            self.estate.upgrade()
        self.player.money = 1000
        self.assertEqual(self.estate.fee, self.fees[0])
        self.estate.upgrade()
        self.assertEqual(self.estate.fee, self.fees[1])
        self.assertEqual(self.player.money, 1000 - self.estate.upgrade_value)


class TestPlaceEstateBlock(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_block_fee_calc_should_calculate_rightly(self):
        block = PlaceEstateBlock('block1')
        place1 = PlaceEstate('杭州', [100, 200, 300, 400],
                             2000, 1000, 300, block)
        place2 = PlaceEstate('厦门', [100, 200, 300, 400],
                             3000, 2000, 300, block)
        place3 = PlaceEstate('苏州', [100, 200, 300, 400],
                             3000, 2000, 300, block)

        player = BasePlayer('邓哲', 20000)
        place1.buy(player)
        place1.upgrade()
        place2.buy(player)
        self.assertEqual(block.block_fee_calc(player), 300)
        place3.buy(player)
        self.assertEqual(block.block_fee_calc(player), 400)

