# -*- coding: utf-8 -*
'''pygame render
'''
from typing import Any, List

import pygame  # type: ignore
import richman.lib.esper as esper  # type: ignore

import richman.core.component as compo


class Renderable:
    def __init__(self, image: pygame.Surface):
        self.image = image
        self.w = image.get_width()
        self.h = image.get_height()


class ProcessorRender(esper.Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        self.window = window
        self.clear_color = clear_color

    def process(self, time_dt: float):
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        entities = self.world.get_components(Renderable,
                                             compo.Position)
        for _, (render, position) in entities:
            self.window.blit(render.image, (position.pos_x, position.pos_y))
        # Flip the framebuffers
        pygame.display.flip()

