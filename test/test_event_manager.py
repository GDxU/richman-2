# -*- coding: utf-8 -*

import unittest
from unittest.mock import MagicMock

import richman.event_manager as em
import richman.interface as itf


class TestEventManaer(unittest.TestCase):

    def setUp(self):
        self.event_manager = em.EventManager()

    def tearDown(self):
        pass

    def test_event_manager_should_add_and_remove_listeners_correctly(self):
        handlers = [MagicMock(), MagicMock(), MagicMock()]
        name = 'Event Test'
        self.event_manager.add_listeners(name, handlers)
        self.assertDictEqual({name: handlers}, self.event_manager.handlers_dict)
        self.event_manager.remove_listeners(name, handlers)
        self.assertFalse(self.event_manager.handlers_dict)

    def test_event_manager_should_send_event_correctly(self):
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
        for handler1 in handlers1:
            handler1.reset_mock()
        for handler2 in handlers2:
            handler2.reset_mock()
        self.event_manager.send(event2)
        for handler1 in handlers1:
            handler1.assert_not_called()
        for handler2 in handlers2:
            handler2.assert_called_once()

    def test_event_manager_should_manager_multiple_events(self):
        self.handler_call_list = []
        def handler1(event):
            self.assertEqual(event.name, 'event1')
            self.handler_call_list.append('handler1')
        def handler2(event):
            self.handler_call_list.append('handler2')
        self.is_handler3_called = False
        def handler3(event):
            self.assertEqual(event.name, 'event2')
            if not self.is_handler3_called:
                self.is_handler3_called = True
                event3 = MagicMock()
                event3.name = 'event1'
                self.event_manager.send(event3)
            self.handler_call_list.append('handler3')
        event1 = MagicMock()
        event1.name = 'event1'
        event2 = MagicMock()
        event2.name = 'event2'
        self.event_manager.add_listeners(event1.name, handler1)
        self.event_manager.add_listeners(event2.name, handler2)
        self.event_manager.add_listeners(event2.name, handler3)

        self.event_manager.send(event2)
        handler_call_list = ['handler2', 'handler3', 'handler1']
        self.assertListEqual(handler_call_list, self.handler_call_list)
