# -*- coding: utf-8 -*
'''事件类，处理全局事件
'''
import logging


class BaseEvent:

    def __init__(self, event_name: str):
        '''init
        
        :param event_name: name of event, str
        '''
        self.__event_name = event_name

    @property
    def event_name(self):
        return self.__event_name


class EventManager:

    def __init__(self):
        self.__handlers_dict = {}  # struct: {event_name1: [handler1, handler2, ...],
                                   #          event_name2: [handler1, handler2, ...], ...}

    @property
    def handlers_dict(self):
        return self.__handlers_dict

    def __event_process(self, event: BaseEvent):
        '''process event
        
        :param event: the event to process
        '''
        if event.event_name in self.__handlers_dict:
            for handler in self.__handlers_dict[event.event_name]:
                handler(event)

    def _add_listener(self, event_name: str, handler):
        '''add handler to the event_name list

        :param event_name: type of event, str
        :param handler: handler to process the event
        '''
        if event_name not in self.__handlers_dict:
            self.__handlers_dict[event_name] = []
        if handler not in self.__handlers_dict[event_name]:
            self.__handlers_dict[event_name].append(handler)
            logging.debug('add {} of {} into event manager.'.format(event_name, handler))

    def add_listeners(self, event_name: str, handlers: list):
        '''add handler to the event_name list

        :param event_name: type of event, str
        :param handlers: handlers to process the event
        '''
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            self._add_listener(event_name, handler)

    def _remove_listener(self, event_name: str, handler):
        '''remove handler from the event_name list

        :param event_name: type of event, str
        :param handler: handler to process the event
        '''
        assert event_name in self.__handlers_dict, '没有类型为 {} 的事件。'.format(event_name)
        self.__handlers_dict[event_name].remove(handler)
        if not self.__handlers_dict[event_name]:
            del self.__handlers_dict[event_name]

    def remove_listeners(self, event_name: str, handlers: list):
        '''remove handler from the event_name list

        :param event_name: type of event, str
        :param handlers: handlers to process the event
        '''
        if not isinstance(handlers, list):
            handlers = [handlers]
        for handler in handlers:
            self._remove_listener(event_name, handler)

    def send(self, event: BaseEvent):
        '''send the event to handlers

        :param event: the event to send
        '''
        self.__event_process(event)

