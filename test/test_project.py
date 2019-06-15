# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock


import richman.project as project 


class TestBaseProject(unittest.TestCase):

    def setUp(self):
        self.project = project.BaseProject(name='核能发电站', buy_value=3500, sell_value = 3000)
    
    def tearDown(self):
        pass

    def test_base_project_buy_should_buy_by_player(self):
        player = MagicMock()
        player.add_money = MagicMock()
        if self.project.owner is None:
            self.project.buy(player)
        player.add_money.assert_called_once()
        self.assertIsNotNone(self.project.owner)


class TestOtherPoject(unittest.TestCase):

    def test_nuclear_project_should_take_effect_to_player(self):
        p = project.ProjectNuclear()
        player = MagicMock()
        player.add_money = MagicMock()
        player.estate_max_level = 3
        p._take_effect(player)
        player.add_money.assert_called_once_with(2000)

    def test_builder_project_should_take_effect_to_player(self):
        p = project.ProjectBuilder()
        player = MagicMock()
        player.add_money = MagicMock()
        player.trigger_upgrade_any_estate = MagicMock()
        p._take_effect(player)
        player.trigger_upgrade_any_estate.assert_called_once()

    
