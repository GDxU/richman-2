# -*- coding: utf-8 -*
'''processor
'''
from typing import Any, List, Type, Tuple
import math

import richman.lib.esper as esper  # type: ignore

import richman.core.component as compo


class ProcessorMovement(esper.Processor):
    '''do the movement by adding velocity to render position
    '''

    def process(self, time_dt: float)->None:
        entities = self.world.get_components(compo.Velocity,
                                             compo.Position)
        for _, (velocity, position) in entities:
            position.pos_x += round(velocity.x)
            position.pos_y += round(velocity.y)


class ProcessorMoveTo(esper.Processor):
    '''move player to position
    '''

    def __init__(self, dst_x: int, dst_y: int)->None:
        self.dst_x = dst_x
        self.dst_y = dst_y
        self.MAX_VELOCITY = 30  # pixel per second
        self.POS_EUQAL_THRESHOLD = 1

    def _distance_calculate(self, delta: Tuple[float, float])->float:
        return math.sqrt(delta[0]*delta[0] + delta[1]*delta[1])

    def _velocity_calulate(self, dt: float,
                           src_pos:Tuple[float, float],
                           dst_pos:Tuple[float, float])->Tuple[bool, float, float]:
        delta_x = dst_pos[0] - src_pos[0]
        delta_y = dst_pos[1] - src_pos[1]
        distance = self._distance_calculate((delta_x, delta_y))
        if distance < self.POS_EUQAL_THRESHOLD:
            return (True, 0., 0.)
        if distance < self.MAX_VELOCITY * dt:
            assert dt > 0
            velocity = distance / dt
        else:
            velocity = self.MAX_VELOCITY
        assert distance > 0
        velocity_x = velocity * delta_x / distance
        velocity_y = velocity * delta_y / distance
        return (False, velocity_x, velocity_y)

    def process(self, time_dt: float)->None:
        entities = self.world.get_components(compo.InputKeyboard,
                                             compo.Velocity,
                                             compo.Position)
        for entity, (_, velocity, position) in entities:
            src_pos = (position.pos_x, position.pos_y)
            dst_pos = (self.dst_x, self.dst_y)
            is_arrived, velocity.x, velocity.y = \
                self._velocity_calulate(time_dt,
                                        src_pos,
                                        dst_pos)
            if is_arrived:
                self.world.remove_component(entity, compo.Velocity)


class ProcessorInputKeyboard(esper.Processor):

    def process(self, time_dt: float)->None:
        entities = self.world.get_components(compo.InputKeyboard,
                                             compo.Velocity)
        for _, (input_keyboard, velocity) in entities:
            if input_keyboard.key_left_pressed:
                velocity.x = -3
            elif input_keyboard.key_right_pressed:
                velocity.x = 3
            else:
                velocity.x = 0
            if input_keyboard.key_down_pressed:
                velocity.y = 3
            elif input_keyboard.key_up_pressed:
                velocity.y = -3
            else:
                velocity.y = 0


