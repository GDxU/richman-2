# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

import richman.event as event


class TestEventManaer(unittest.TestCase):

    def setUp(self):
        self.event_manager = event.EventManager()

    def tearDown(self):
        pass

    def test_event_manager_should_add_and_remove_listeners_correctly(self):
        handlers = [MagicMock(), MagicMock(), MagicMock()]
        name = 'Event Test'
        self.event_manager.add_listeners(name, handlers)
        self.assertDictEqual({name: handlers}, self.event_manager.handlers_dict)
        self.event_manager.remove_listeners(name, handlers)
        self.assertFalse(self.event_manager.handlers_dict)

    def test_event_manager_sould_send_event_correctly(self):
        handlers1 = [MagicMock(), MagicMock(), MagicMock()]
        event_name1 = 'Event Test 1'
        self.event_manager.add_listeners(event_name1, handlers1)
        handlers2 = [MagicMock(), MagicMock(), MagicMock()]
        event_name2 = 'Event Test 2'
        self.event_manager.add_listeners(event_name2, handlers2)

        event1 = MagicMock()
        event1.name = event_name1
        self.event_manager.send(event1)
        for handler1 in handlers1:
            handler1.assert_called_once()
        for handler2 in handlers2:
            handler2.assert_not_called()

        event2 = MagicMock()
        event2.name = event_name2
        self.event_manager.send(event2)
        for handler1 in handlers1:
            handler1.assert_not_called()
        for handler2 in handlers2:
            handler2.assert_called_once()