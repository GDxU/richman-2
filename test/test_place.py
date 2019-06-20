# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


import richman.place as place
import richman.event as ev


class TestEstate(unittest.TestCase):

    def setUp(self):
        self.block = MagicMock()
        self.fees = [100, 200, 300, 400]
        self.estate = place.Estate(name='Hangzhou',
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
        with self.assertRaises(AssertionError):
            ev.event_to_estate_pledge.send(player, receiver=self.estate)
        ev.event_to_place_buy.send(player, receiver=self.estate)
        ev.event_to_estate_pledge.send(player, receiver=self.estate)
        with self.assertRaises(AssertionError):
            ev.event_to_estate_pledge.send(player, receiver=self.estate)

    def test_two_place_eq_check(self):
        estate1 = place.Estate(name='Hangzhou',
                               fees=self.fees,
                               buy_value=3300,
                               pledge_value=1100,
                               upgrade_value=600,
                               block=MagicMock())
        estate2 = place.Estate(name='Xiamen',
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
            place.Estate('杭州', fees,
                         2000, 1000, 300, self.block)

    def test_upgrade_should_run_correctly_and_raise_exception(self):
        player = MagicMock()
        ev.event_to_place_buy.send(player, receiver=self.estate)

        self.assertEqual(self.estate.fee, self.fees[0])
        ev.event_to_estate_upgrade.send(player, receiver=self.estate)
        self.assertEqual(self.estate.fee, self.fees[1])


class TestEstateBlock(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass
    
    def test_block_fee_calc_should_calculate_rightly(self):
        block = place.EstateBlock('block1')
        place1 = place.Estate('杭州', [100, 200, 300, 400],
                              2000, 1000, 300, block)
        place2 = place.Estate('厦门', [100, 200, 300, 400],
                              3000, 2000, 300, block)
        place3 = place.Estate('苏州', [100, 200, 300, 400],
                              3000, 2000, 300, block)
        player = MagicMock()
        ev.event_to_place_buy.send(player, receiver=place1)
        ev.event_to_estate_upgrade.send(player, receiver=place1)
        ev.event_to_place_buy.send(player, receiver=place2)
        self.assertEqual(block.block_fee_calc(player), 300)
        ev.event_to_place_buy.send(player, receiver=place3)
        self.assertEqual(block.block_fee_calc(player), 400)


class TestOtherPoject(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_nuclear_project_should_take_effect_to_player(self):
        p = place.ProjectNuclear()
        p._exchange_money = MagicMock()
        player = MagicMock()
        p.event_handler_buy(player, receiver=p)
        player.estate_max_level = 3
        p._take_effect(player)
        p._exchange_money.assert_called_once_with(player, p.owner, 2000)

    def test_builder_project_should_take_effect_to_player(self):
        p = place.ProjectBuilder()
        player = MagicMock()
        player.name = 'player that has the builder project.'
        estate = MagicMock()
        estate.owner = MagicMock()
        estate.owner.name = 'player that upgrades the estate.'
        p._buy(player)
        ev.event_from_estate_upgraded.send(estate)
        # upgrade and estat test
        event_handler_upgrade_estate = MagicMock()
        with ev.event_to_player_upgrade_any_estate.connected_to(event_handler_upgrade_estate):
            p._take_effect(player)
            event_handler_upgrade_estate.assert_called_once()
        # take fee for upgrade estate
        p._exchange_money = MagicMock()
        ev.event_from_estate_upgraded.send(estate)
        p._exchange_money.assert_called_once_with(estate.owner, p.owner, 500)
