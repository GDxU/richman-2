# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


import richman.estate as estate
import richman.event as ev


class TestEstate(unittest.TestCase):

    def setUp(self):
        self.block = MagicMock()
        self.fees = [100, 200, 300, 400]
        self.event_manager = MagicMock()
        self.event_manager.send = MagicMock()
        self.estate = estate.Estate(event_manager=self.event_manager,
                                    name='Hangzhou',
                                    fees=self.fees,
                                    buy_value=2200,
                                    pledge_value=1100,
                                    upgrade_value=600,
                                    block=self.block)
    
    def tearDown(self):
        pass

    def test_estate_init_should_set_vars_properly(self):
        self.assertEqual(self.estate.name, 'Hangzhou')
        self.assertEqual(self.estate.buy_value, 2200)
        self.assertEqual(self.estate.pledge_value, 1100)

    def test_estate_pledge_should_execute_correctlly(self):
        player = MagicMock()
        event_pledge = MagicMock()
        event_pledge.player = player
        with self.assertRaises(AssertionError):
            self.estate.event_handler_pledge(event_pledge)
        event_buy = MagicMock()
        event_buy.player = player
        self.estate.event_handler_buy(event_buy)
        self.estate.event_handler_pledge(event_pledge)
        with self.assertRaises(AssertionError):
            self.estate.event_handler_pledge(event_pledge)

    def test_two_place_eq_check(self):
        estate1 = estate.Estate(event_manager=self.event_manager,
                                name='Hangzhou',
                                fees=self.fees,
                                buy_value=3300,
                                pledge_value=1100,
                                upgrade_value=600,
                                block=MagicMock())
        estate2 = estate.Estate(event_manager=self.event_manager,
                                name='Xiamen',
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
            estate.Estate(self.event_manager, '杭州', fees,
                          2000, 1000, 300, self.block)

    def test_upgrade_should_run_correctly_and_raise_exception(self):
        event = MagicMock()
        event.player = MagicMock()
        self.estate.event_handler_buy(event)

        self.assertEqual(self.estate.fee, self.fees[0])
        self.estate.event_handler_upgrade(event)
        self.assertEqual(self.estate.fee, self.fees[1])


class TestEstateBlock(unittest.TestCase):
    
    def setUp(self):
        self.event_manager = MagicMock()
    
    def tearDown(self):
        pass
    
    def test_block_fee_calc_should_calculate_rightly(self):
        block = estate.EstateBlock('block1')
        place1 = estate.Estate(self.event_manager,
                               '杭州', [100, 200, 300, 400],
                               2000, 1000, 300, block)
        place2 = estate.Estate(self.event_manager,
                               '厦门', [100, 200, 300, 400],
                               3000, 2000, 300, block)
        place3 = estate.Estate(self.event_manager,
                               '苏州', [100, 200, 300, 400],
                               3000, 2000, 300, block)
        event = MagicMock()
        event.player = MagicMock()
        place1.event_handler_buy(event)
        place1.event_handler_upgrade(event)
        place2.event_handler_buy(event)
        self.assertEqual(block.block_fee_calc(event.player), 300)
        place3.event_handler_buy(event)
        self.assertEqual(block.block_fee_calc(event.player), 400)

