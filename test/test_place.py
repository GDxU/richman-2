# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


import richman.place as place
import richman.event as ev


class TestEstate(unittest.TestCase):

    def setUp(self):
        self.block = MagicMock()
        self.fees = [100, 200, 300, 400]
        self.event_manager = MagicMock()
        self.event_manager.send = MagicMock()
        self.estate = place.Estate(event_manager=self.event_manager,
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
        estate1 = place.Estate(event_manager=self.event_manager,
                                name='Hangzhou',
                                fees=self.fees,
                                buy_value=3300,
                                pledge_value=1100,
                                upgrade_value=600,
                                block=MagicMock())
        estate2 = place.Estate(event_manager=self.event_manager,
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
            place.Estate(self.event_manager, '杭州', fees,
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
        block = place.EstateBlock('block1')
        place1 = place.Estate(self.event_manager,
                               '杭州', [100, 200, 300, 400],
                               2000, 1000, 300, block)
        place2 = place.Estate(self.event_manager,
                               '厦门', [100, 200, 300, 400],
                               3000, 2000, 300, block)
        place3 = place.Estate(self.event_manager,
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


class TestOtherPoject(unittest.TestCase):

    def setUp(self):
        self.event_manager = MagicMock()
    
    def tearDown(self):
        pass

    def test_nuclear_project_should_take_effect_to_player(self):
        p = place.ProjectNuclear()
        player = MagicMock()
        player.add_money = MagicMock()
        player.estate_max_level = 3
        p._take_effect(player)
        player.add_money.assert_called_once_with(2000)

    def test_builder_project_should_take_effect_to_player(self):
        p = place.ProjectBuilder()
        player = MagicMock()
        player.add_money = MagicMock()
        player.trigger_upgrade_any_estate = MagicMock()
        p._take_effect(player)
        player.trigger_upgrade_any_estate.assert_called_once()
