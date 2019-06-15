# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


import richman.estate as estate


class TestEstate(unittest.TestCase):

    def setUp(self):
        self.block = MagicMock()
        self.fees = [100, 200, 300, 400]
        self.estate = estate.Estate(name='Hangzhou',
                                    fees=self.fees,
                                    buy_value=2200,
                                    pledge_value=1100,
                                    upgrade_value=600,
                                    block=self.block)
        self.player = MagicMock()
        self.player.add_money = MagicMock()
        self.player.trigger_buy = MagicMock()
    
    def tearDown(self):
        pass

    def test_estate_init_should_set_vars_properly(self):
        self.assertEqual(self.estate.name, 'Hangzhou')
        self.assertEqual(self.estate.buy_value, 2200)
        self.assertEqual(self.estate.pledge_value, 1100)

    def test_buy_and_rebuy_should_raise_execption(self):
        self.player.add_money = MagicMock()
        self.estate.buy(self.player)
        self.player.add_money.assert_called_once()
        with self.assertRaises(AssertionError):
            self.estate.rebuy()

    def test_estate_pledge_should_execute_correctlly(self):
        with self.assertRaises(AssertionError):
            self.estate.pledge()
        self.estate.buy(self.player)
        self.estate.pledge()
        with self.assertRaises(AssertionError):
            self.estate.pledge()

    def test_two_place_eq_check(self):
        estate1 = estate.Estate(name='Hangzhou',
                                fees=self.fees,
                                buy_value=3300,
                                pledge_value=1100,
                                upgrade_value=600,
                                block=MagicMock())
        estate2 = estate.Estate(name='Xiamen',
                               fees=self.fees,
                               buy_value=3300,
                               pledge_value=1100,
                               upgrade_value=600,
                               block=MagicMock())
        self.assertEqual(self.estate, estate1)
        self.assertNotEqual(self.estate, estate2)

    def test_fees_should_go_up_with_level_up(self):
        fees = [100, 20, 300, 400]
        with self.assertRaises(AssertionError):
            estate.Estate('杭州', fees,
                          2000, 1000, 300, self.block)

    def test_upgrade_should_run_correctly_and_raise_exception(self):
        self.estate.buy(self.player)
        self.player.add_money.assert_called()
        self.assertEqual(self.estate.fee, self.fees[0])
        self.estate.upgrade()
        self.player.add_money.assert_called()
        self.assertEqual(self.estate.fee, self.fees[1])

    def test_add_to_static_callbacks_upgrade_should_add_callbacks_staticlly(self):
        callbacks = [MagicMock(), MagicMock(), MagicMock()]
        for callback in callbacks:
            estate.Estate.add_to_static_callbacks_upgrade(callback)
        self.estate.buy(self.player)
        self.estate.upgrade()
        for callback in callbacks:
            callback.assert_called_once()


class TestEstateBlock(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_block_fee_calc_should_calculate_rightly(self):
        block = estate.EstateBlock('block1')
        place1 = estate.Estate('杭州', [100, 200, 300, 400],
                               2000, 1000, 300, block)
        place2 = estate.Estate('厦门', [100, 200, 300, 400],
                               3000, 2000, 300, block)
        place3 = estate.Estate('苏州', [100, 200, 300, 400],
                               3000, 2000, 300, block)
        player = MagicMock()
        place1.buy(player)
        place1.upgrade()
        place2.buy(player)
        self.assertEqual(block.block_fee_calc(player), 300)
        place3.buy(player)
        self.assertEqual(block.block_fee_calc(player), 400)

