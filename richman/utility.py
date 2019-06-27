# -*- coding: utf-8 -*
'''utility
'''
from typing import Any, List, Dict, Callable, Optional, Iterable, Deque, cast
import logging
from copy import copy
from copy import deepcopy
from uuid import uuid4
from collections import deque
import random
import datetime


class RollbackException(RuntimeError):
    '''occurs when rollback
    '''
    pass


def _memento(obj: object, deep:bool = False)->Callable:
    '''realize the core function of memento

    :param obj: python obj
    :param deep: if deep copy
    '''
    state = deepcopy(obj.__dict__) if deep else copy(obj.__dict__)

    def restore()->None:
        obj.__dict__.clear()
        obj.__dict__.update(state)
        logging.debug('obj to rollback: {}'.format(obj))

    return restore


class Transaction:
    """A transaction guard.
    This is, in fact, just syntactic sugar around a _memento closure.
    """

    def __init__(self, deep: bool, objs: List[object],
                 rollback_len:int = 1, uid:Optional[str] = None)->None:
        '''init

        :param deep: if deep copy
        :param objs: list of object to use memento
        :param rollback_len: the max rollback length
        :param uid: unique id of the transction
        '''
        if not isinstance(objs, list):
            objs = cast(List[object], [objs])
        self.__deep = deep
        self.__objs = objs
        self.__uid = uid
        if self.__uid is None:
            self.__uid = str(uuid4())
        StatesType = List[Callable]
        self.__copies:Deque[StatesType] = deque(maxlen=rollback_len)
        self.commit()

    @property
    def uid(self)->Optional[str]:
        return self.__uid

    def commit(self)->None:
        '''commit objects state to memento
        '''
        logging.warning('%s state is committed...' % self.__uid)
        states = [_memento(obj, self.__deep) for obj in self.__objs]
        logging.debug('obj to commit: {}'.format([str(obj) for obj in self.__objs]))
        self.__copies.append(states)

    def rollback(self, step:int = 1)->None:
        '''rollback state in memento

        :param step: step to rollback
        '''
        assert step >= 1
        logging.debug('step is %i' % step)
        logging.warning('%s is now rollbacking...' % self.__uid)
        for _ in range(step-1):
            self.__copies.pop()
        states = self.__copies.pop()
        for state in states:
            state()


class Transactional:
    """Adds transactional semantics to methods. Methods decorated  with
    @Transactional will rollback to entry-state upon exceptions.

    example:

    class NumObj(object):
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return '<%s: %r>' % (self.__class__.__name__, self.value)

        def increment(self):
            self.value += 1

        @Transactional
        def do_stuff(self):
            self.value = '1111'  # <- invalid value
            self.increment()  # <- will fail and rollback automativly
    """

    def __init__(self, method: Callable):
        '''
        '''
        self.__method = method

    def __get__(self, obj, T):
        def transaction(*args, **kwargs):
            state = _memento(obj)
            try:
                return self.__method(obj, *args, **kwargs)
            except Exception as e:
                state()
                raise e

        return transaction



class MapTopology:
    '''descriptoin of topology for the map
    '''
    
    def __init__(self, map)->None:
        self.__pre_pos = 0
        self.__current_pos = 0
        self._build_map_topo(map)

    def _build_map_topo(self, map):
        self.name = 'Map Testing'
        # init turn_points
        # None means divert to anywhere
        # treat it as -1 when calculating within a process
        self.turn_points: Dict[int, int] =\
            {13: None,
             23: 10,
             24: None,
             33: None}
        self.map_len = 40

    @property
    def pos(self):
        return self.__current_pos

    def go(self, step: int)->int:
        '''go forward with step

        :param step: step to go
        '''
        assert step > 0
        self.__pre_pos += step
        self.__pre_pos = self.__pre_pos % self.map_len
        self.__current_pos = self.__pre_pos
        self.divert()  # divert if at the turn_points
        return self.__current_pos

    def divert(self)->None:
        '''divert if the pos stands at turn_point
        '''
        if self.__pre_pos in self.turn_points:
            pos_dst = self.turn_points[self.__pre_pos]
            self.__pre_pos = pos_dst if pos_dst else -1

    def __len__(self)->int:
        return self.map_len


class MapStatistics:
    '''calculate the statics of the map
    '''
    
    def __init__(self, map_topo: MapTopology)->None:
        '''init the topology of the map

        :param map_topo: topology of the map in MapTopology form
        '''
        self.map_topo = map_topo

    def calculate_trigger_rate(self, dice_max:int = 6,
                               rounds:int = 500000)->List[int]:
        '''calculate the trigger rate for each item in the map

        :param dice_max: the max num the dice can display
        :param rounds: the number of rounds to test
        '''
        random.seed(datetime.datetime.now())
        rsts:list = [0 for _ in range(len(self.map_topo))]
        for _ in range(rounds):
            dice_num = random.randrange(1,dice_max+1)
            pos = self.map_topo.go(step=dice_num)
            rsts[pos] += 1
        return [rst/rounds for rst in rsts]
