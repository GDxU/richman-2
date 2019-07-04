# -*- coding: utf-8 -*-
'''main app
'''
import pygame
import richman.core.esper as esper

import richman.core.component as compo
import richman.core.processor as proc
import richman.core.pygame_render as render


FPS = 60
RESOLUTION = 720, 480


def run():
    # Initialize Pygame stuff
    pygame.init()
    window = pygame.display.set_mode(RESOLUTION)
    pygame.display.set_caption("Esper Pygame example")
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 1)

    # Initialize Esper world, and create a "player" Entity with a few Components.
    world = esper.World()
    player = world.create_entity()
    world.add_component(player, compo.Player(name='dengzhe'))
    world.add_component(player, compo.Velocity(x=0))
    world.add_component(player, render.Renderable(image=pygame.image.load("redsquare.png"), x=100))
    # Another motionless Entity:
    enemy = world.create_entity()
    world.add_component(enemy, render.Renderable(image=pygame.image.load("bluesquare.png"), x=400))

    # Create some Processor instances, and asign them to be processed.
    processor_render = render.ProcessorRender(window=window)
    processor_movement = proc.MovementProcessor(x_max=RESOLUTION[0], render_type=render.Renderable)
    world.add_processor(processor_render)
    world.add_processor(processor_movement)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    # Here is a way to directly access a specific Entity's
                    # Velocity Component's attribute (y) without making a
                    # temporary variable.
                    world.component_for_entity(player, compo.Velocity).x = -3
                elif event.key == pygame.K_RIGHT:
                    # For clarity, here is an alternate way in which a
                    # temporary variable is created and modified. The previous
                    # way above is recommended instead.
                    player_velocity_component = world.component_for_entity(player, compo.Velocity)
                    player_velocity_component.x = 3
                elif event.key == pygame.K_UP:
                    world.component_for_entity(player, compo.Velocity).y = -3
                elif event.key == pygame.K_DOWN:
                    world.component_for_entity(player, compo.Velocity).y = 3
                elif event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    world.component_for_entity(player, compo.Velocity).x = 0
                if event.key in (pygame.K_UP, pygame.K_DOWN):
                    world.component_for_entity(player, compo.Velocity).y = 0

        # A single call to world.process() will update all Processors:
        world.process()

        clock.tick(FPS)


if __name__ == "__main__":
    run()
    pygame.quit()
