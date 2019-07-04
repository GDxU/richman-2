# -*- coding: utf-8 -*
'''entity and system
'''
from typing import Any, List
import abc

import richman.lib.esper as esper  # type: ignore


class Player:
    def __init__(self, name: str)->None:
        self.name = name

class Velocity:
    def __init__(self, x:int = 0)->None:
        self.x = x
