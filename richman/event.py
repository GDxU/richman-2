# -*- coding: utf-8 -*
'''事件类，处理全局事件
'''
import logging


class BaseEvent:

    def __init__(self, event_type: str):
        '''init
        
        :param event_type: type of event, str
        '''
        self.__event_type = event_type

    @property
    def event_type(self):
        return self.__event_type


class EventManager:

    def __init__(self):
        self.__handlers = {}  # struct: {event_type: [handler1, handler2, ...], ...}

    def __event_process(self, event: BaseEvent):
        '''process event
        
        :param event: the event to process
        '''
        if event.event_type in self.__handlers:
            for handler in self.__handlers[event.event_type]:
                handler(event)

    def add_listener(self, event_type: str, handler):
        '''add handler to the event_type list

        :param event_type: type of event, str
        :param handler: handle to process the event
        '''
        if event_type not in self.__handlers:
            self.__handlers[event_type] = []
        if handler not in self.__handlers[event_type]:
            self.__handlers[event_type].append(handler)
            logging.debug('add {} of {} into event manager.'.format(event_type, handler))

    def remove_listener(self, event_type: str, handler):
        '''remove handler from the event_type list

        :param event_type: type of event, str
        :param handler: handle to process the event
        '''
        assert event_type in self.__handlers, '没有类型为 {} 的事件。'.format(event_type)
        self.__handlers[event_type].remove(handler)
        if not self.__handlers[event_type]:
            del self.__handlers[event_type]

    def send(self, event: BaseEvent):
        '''send the event to handlers

        :param event: the event to send
        '''
        self.__event_process(event)

