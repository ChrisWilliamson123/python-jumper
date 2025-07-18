from dataclasses import dataclass

import pygame

from gameutils.ecs.component import Component

@dataclass
class Sprite(Component):
    sprite: pygame.sprite.Sprite
