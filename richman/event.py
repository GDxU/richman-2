# -*- coding: utf-8 -*
'''事件类，处理全局事件
'''
import logging


class BaseEvent:

    def __init__(self, name: str):
        '''init
        
        :param name: name of event, str
        '''
        self.__event_name = name

    @property
    def name(self):
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

    def send(self, event: BaseEvent):
        '''send the event to handlers

        :param event: the event to send
        '''
        self.__event_process(event)

