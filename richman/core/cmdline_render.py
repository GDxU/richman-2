# -*- coding: utf-8 -*
'''command line render
'''
from typing import Any, List

import richman.lib.esper as esper  # type: ignore

import richman.core.component as compo


class Renderable:
    def __init__(self, x: int):
        self.x = x


class ProcessorRender(esper.Processor):
    def __init__(self):
        pass

    def process(self):
        # Clear the window:
        self._clear()
        # This will iterate over every Entity that has this Component, and blit it:
        for _, rend in self.world.get_component(Renderable):
            self._blit()
        self._flip()

    def _clear(self):
        pass
    
    def _blit(self):
        pass

    def _flip(self):
        '''flip the framebuffers
        '''
        pass
