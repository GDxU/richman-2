# -*- coding: utf-8 -*
'''processor
'''
from typing import Any, List, Type

import richman.core.esper as esper

import richman.core.component as compo


class MovementProcessor(esper.Processor):
    def __init__(self, x_max: int, render_type: Type[Any]):
        self.x_max = x_max
        self.render_type = render_type

    def process(self):
        objects = self.world.get_components(compo.Velocity,
                                            self.render_type)
        for _, (velocity, render) in objects:
            render.x += velocity.x

