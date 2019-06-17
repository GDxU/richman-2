# -*- coding: utf-8 -*
'''事件类，处理全局事件

非线程安全
'''
import queue
import logging

import richman.interface as itf


class EventManager:

    def __init__(self):
        self.__events = []  # use list to perform as a queue
        self.__handlers_dict = {}  # struct: {event_name1: [handler1, handler2, ...],
                                   #          event_name2: [handler1, handler2, ...], ...}

    @property
    def handlers_dict(self):
        return self.__handlers_dict

    def __insert_event(self, event: itf.IEventManagerForEvent):
        '''insert event to the storage

        :param event: itf.IEventManagerForEvent
        '''
        if len(self.__events) > 100:
            raise RuntimeError('未处理事件累计超过最大值，该状态不正常！')
        self.__events.append(event)

    def __pop_event(self)->itf.IEventManagerForEvent:
        '''pop up the lastest event

        :return: itf.IEventManagerForEvent or IteratorStop Exception
        '''
        while self.__events:
            yield self.__events.pop(0)

    def __process_event(self):
        '''process event
        
        :param event: the event to process
        '''
        for event in self.__pop_event():
            if event.name in self.__handlers_dict:
                for handler in self.__handlers_dict[event.name]:
                    handler(event)

    def _add_listener(self, name: str, handler):
        '''add handler to the name list

        :param name: type of event, str
        :param handler: handler to process the event
        '''
        if name not in self.__handlers_dict:
            self.__handlers_dict[name] = []
        if handler not in self.__handlers_dict[name]:
            self.__handlers_dict[name].append(handler)
            logging.debug('add {} of {} into event manager.'.format(name, handler))

    def add_listeners(self, name: str, handlers: list):
        '''add handler to the name list

        :param name: type of event, str
        :param handlers: handlers to process the event
        '''
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            self._add_listener(name, handler)

    def _remove_listener(self, name: str, handler):
        '''remove handler from the name list

        :param name: type of event, str
        :param handler: handler to process the event
        '''
        assert name in self.__handlers_dict, '没有类型为 {} 的事件。'.format(name)
        self.__handlers_dict[name].remove(handler)
        if not self.__handlers_dict[name]:
            del self.__handlers_dict[name]

    def remove_listeners(self, name: str, handlers: list):
        '''remove handler from the name list

        :param name: type of event, str
        :param handlers: handlers to process the event
        '''
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            self._remove_listener(name, handler)

    def send(self, event: itf.IEventManagerForEvent):
        '''send the event to handlers

        :param event: the event to send
        '''
        logging.debug('send event of {}'.format(event.name))
        self.__insert_event(event)
        self.__process_event()

