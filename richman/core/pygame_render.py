# -*- coding: utf-8 -*
'''pygame render
'''
from typing import Any, List

import pygame  # type: ignore
import richman.lib.esper as esper  # type: ignore

import richman.core.component as compo


class Renderable:
    def __init__(self, image: pygame.Surface,
                 x: int, depth:int = 0):
        self.image = image
        self.depth = depth
        self.x = x
        self.w = image.get_width()
        self.h = image.get_height()


class ProcessorRender(esper.Processor):
    def __init__(self, window, clear_color=(0, 0, 0)):
        self.window = window
        self.clear_color = clear_color

    def process(self):
        # Clear the window:
        self.window.fill(self.clear_color)
        # This will iterate over every Entity that has this Component, and blit it:
        for _, rend in self.world.get_component(Renderable):
            self.window.blit(rend.image, (rend.x, 0.5*rend.w))
        # Flip the framebuffers
        pygame.display.flip()

