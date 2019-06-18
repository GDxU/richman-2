# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

import richman.event as ev


class TestBaseEvent(unittest.TestCase):

    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test__build_name_should_build_different_name_with_different_class(self):
        ev1 = ev.EventToPlaceBuy('hehe', 1)
        ev2 = ev.EventToPlayerAddMoney('hehe', 1)
        self.assertNotEqual(ev1.name, ev2.name)
