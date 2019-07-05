# -*- coding: utf-8 -*-
'''main app
'''
import os
from typing import Tuple, Optional, Any, List

import pygame  # type: ignore
from pygame.locals import *
from pygame.compat import geterror
import richman.lib.esper as esper  # type: ignore

import richman.core.component as compo
import richman.core.processor as proc
import richman.core.pygame_render as render


class App:

    MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]
    PIC_DIR = os.path.join(MAIN_DIR, 'pic')
    PROC_INPUT_KEYBOARD_PRIORITY = 4  # the more the higher
    PROC_MOVEMENT_PRIORITY = 3

    def __init__(self, FPS: int, RESOLUTION: Tuple[int, int]):
        self.FPS = FPS
        self.RESOLUTION = RESOLUTION
        self.running = True
        self._setup_context()

    def _setup_context(self):
        # Initialize Pygame stuff
        pygame.init()
        self.window = pygame.display.set_mode(self.RESOLUTION)
        pygame.display.set_caption("Rich Man")
        pygame.mouse.set_visible(0)

        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(1, 1)
        self.world = self._game_builder()

    def _load_image(self, name: str, colorkey:Optional[int] = None)->pygame.Surface:
        fullname = os.path.join(self.PIC_DIR, name)
        try:
            image = pygame.image.load(fullname)
        except pygame.error:
            raise SystemExit(str(geterror()))
        image = image.convert()
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def _load_sound(self, name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer or not pygame.mixer.get_init():
            return NoneSound()
        fullname = os.path.join(self.PIC_DIR, name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error:
            raise SystemExit(str(geterror()))
        return sound

    def _game_builder(self)->esper.World:
        # self.world
        self.world = esper.World()
        # players
        players:List[int] = []
        # player 1
        player = self.world.create_entity()
        players.append(player)
        self.world.add_component(player, compo.Player(name='邓哲', money=10000))
        self.world.add_component(player, compo.Position(pos_x=100, pos_y=100, index_in_map=0))
        self.world.add_component(player, compo.InputKeyboard())
        self.world.add_component(player, compo.Velocity())
        self.world.add_component(player, render.Renderable(image=self._load_image("dengzhe.png")))
        # player 2
        player = self.world.create_entity()
        players.append(player)
        self.world.add_component(player, compo.Player(name='邓彦修', money=10000))
        self.world.add_component(player, compo.Position(pos_x=100, pos_y=100, index_in_map=0))
        # self.world.add_component(player, compo.InputKeyboard())
        self.world.add_component(player, compo.Velocity())
        self.world.add_component(player, render.Renderable(image=self._load_image("dengyanxiu.png")))

        # places
        places:List[int] = []
        # place 1
        place = self.world.create_entity()
        places.append(place)
        self.world.add_component(place, compo.Place(name='起点'))
        self.world.add_component(place, compo.Position(pos_x=200, pos_y=200, index_in_map=0))
        self.world.add_component(place, render.Renderable(image=self._load_image("start.png")))
        # place 2
        place = self.world.create_entity()
        places.append(place)
        self.world.add_component(place, compo.Place(name='沈阳'))
        self.world.add_component(place, compo.Position(pos_x=300, pos_y=300, index_in_map=1))
        self.world.add_component(place, render.Renderable(image=self._load_image("shenyang.png")))
        # place 3
        place = self.world.create_entity()
        places.append(place)
        self.world.add_component(place, compo.Place(name='天津'))
        self.world.add_component(place, compo.Position(pos_x=400, pos_y=400, index_in_map=2))
        self.world.add_component(place, render.Renderable(image=self._load_image("tianjin.png")))

        # processor input keyboard
        processor_input_keyboard = proc.ProcessorInputKeyboard()
        self.world.add_processor(processor_input_keyboard, priority=self.PROC_INPUT_KEYBOARD_PRIORITY)
        
        # processor movement
        processor_movement = proc.ProcessorMovement()
        self.world.add_processor(processor_movement, priority=self.PROC_MOVEMENT_PRIORITY)

        # processor render
        processor_render = render.ProcessorRender(window=self.window)
        self.world.add_processor(processor_render)

        return self.world

    keyboard_map = {
        pygame.K_LEFT: 'key_left_pressed',
        pygame.K_RIGHT: 'key_right_pressed',
        pygame.K_UP: 'key_up_pressed',
        pygame.K_DOWN: 'key_down_pressed'
    }
    def _input_keyboard_map(self, key_value: int, pressed: bool)->None:
        def set_key_value(input_keyboard, key_name: str, pressed: bool):
            input_keyboard.__dict__[key_name] = pressed
        entities = self.world.get_component(compo.InputKeyboard)
        for _, input_keyboard in entities:
            set_key_value(input_keyboard, self.keyboard_map[key_value], pressed)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self._input_keyboard_map(key_value=event.key, pressed=True)
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                        self._input_keyboard_map(key_value=event.key, pressed=False)

            time_dt = self.clock.get_time() / 1000  # second
            self.world.process(time_dt)
            self.clock.tick(self.FPS)

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    app = App(FPS=60, RESOLUTION=(1080, 720))
    app.run()
    app.quit()
