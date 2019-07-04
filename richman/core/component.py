# -*- coding: utf-8 -*
'''entity and system
'''
from typing import Any, List
import abc

import richman.core.esper as esper


class Player:
    def __init__(self, name: str)->None:
        self.name = name

class Velocity:
    def __init__(self, x:int = 0)->None:
        self.x = x
