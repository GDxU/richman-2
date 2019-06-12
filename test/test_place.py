# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


from richman.place import (
    PlaceImplement,
    PlaceEstate,
    PlaceEstateBlock,
    PledgeWithNoOwnerException,
    PledgeTwiceException,
    RebuyNotPledgedException
)
from richman.player import PlayerImplement
from richman.map import MapImplement


class TestBasePlace(unittest.TestCase):

    def setUp(self):
        self.estate = PlaceImplement(name='Hangzhou',
                                     buy_value=2200,
                                     pledge_value=1100)
        map = MapImplement('china')
        self.player = PlayerImplement('Dengzhe', 100, map)
    
    def tearDown(self):
        pass

    def test_base_place_init_should_set_vars_properly(self):
        self.assertEqual(self.estate.name, 'Hangzhou')
        self.assertEqual(self.estate.buy_value, 2200)
        self.assertEqual(self.estate.pledge_value, 1100)

    def test_buy_and_rebuy_should_raise_execption(self):
        self.player.trigger_buy = MagicMock()
        self.estate.buy(self.player)
        self.player.trigger_buy.assert_called_once()
        with self.assertRaises(RebuyNotPledgedException):
            self.estate.rebuy()

    def test_base_place_pledge_should_execute_correctlly(self):
        self.player.add_money = MagicMock()
        with self.assertRaises(PledgeWithNoOwnerException):
            self.estate.pledge()
        self.estate.buy(self.player)
        self.estate.pledge()
        with self.assertRaises(PledgeTwiceException):
            self.estate.pledge()

    def test_two_place_eq_check(self):
        place1 = PlaceImplement(name='Hangzhou',
                                buy_value=2200,
                                pledge_value=1100)
        place2 = PlaceImplement(name='Xiamen',
                                buy_value=3300,
                                pledge_value=1100)
        self.assertEqual(self.estate, place1)
        self.assertNotEqual(self.estate, place2)


class TestPlaceEstate(unittest.TestCase):
    
    def setUp(self):
        self.block = PlaceEstateBlock('block1')
        self.fees = [100, 200, 300, 400]
        self.estate = PlaceEstate('杭州', self.fees,
                                  2000, 1000, 300, self.block)
        map = MapImplement('china')
        self.player = PlayerImplement('Dengzhe', 100, map)
        self.player.trigger_buy = MagicMock()

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
        self.player.add_money = MagicMock()
        self.estate.upgrade()
        self.player.add_money.assert_called_once()
        self.player.money = 1000
        self.assertEqual(self.estate.fee, self.fees[0])
        self.estate.upgrade()
        self.assertEqual(self.estate.fee, self.fees[1])


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
        map = MapImplement('china')
        player = PlayerImplement('邓哲', 20000, map)
        place1.buy(player)
        place1.upgrade()
        place2.buy(player)
        self.assertEqual(block.block_fee_calc(player), 300)
        place3.buy(player)
        self.assertEqual(block.block_fee_calc(player), 400)

