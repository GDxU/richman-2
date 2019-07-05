# -*- coding: utf-8 -*
'''entity and system
'''
from typing import Any, List
import abc

import richman.lib.esper as esper  # type: ignore


class InputKeyboard:
    def __init__(self)->None:
        self.key_left_pressed = False
        self.key_right_pressed = False
        self.key_up_pressed = False
        self.key_down_pressed = False
        self.key_enter_pressed = False


class Player:
    def __init__(self, name: str, money: int)->None:
        self.name = name
        self.money = money


class Place:
    def __init__(self, name: str)->None:
        self.name = name


class Position:
    def __init__(self, pos_x: int, pos_y: int, index_in_map: int)->None:
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.index_in_map = index_in_map


class ChangeMoney:
    def __init__(self, fee: int)->None:
        self.fee = fee


class Velocity:
    def __init__(self, x:float = 0, y:float = 0)->None:
        self.x = x
        self.y = y
