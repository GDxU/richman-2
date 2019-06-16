# -*- coding: utf-8 -*
'''事件类，处理全局事件
'''
import logging

import richman.interface as itf


class BaseEvent(itf.IForEvent):

    def __init__(self, name):
        self.__name = name
        self.__receivers = []

    @property
    def name(self):
        return self.__name
    @property
    def receivers(self):
        return self.__receivers

    def attach(self, receiver):
        '''attach receiver into event

        :param receiver: receiver to trigger when event occurs
        '''
        if receiver not in self.__receivers:
            self.__receivers.append(receiver)

    def detach(self, receiver):
        '''detach receiver from event

        :param receiver: receiver to trigger when event occurs
        '''
        assert receiver in self.receivers
        self.__receivers.remove(receiver)

    def trigger(self, sender=None):
        '''trigger each receiver for event

        :param sender: the obj that send the event
        '''
        for receiver in self.__receivers:
            if sender != receiver:
                receiver.update(self)


class EventEstateUpgrade(BaseEvent):

    def __init__(self):
        super().__init__(name='estate upgrade occurs')

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.trigger()
