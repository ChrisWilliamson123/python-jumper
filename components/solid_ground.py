from dataclasses import dataclass
import pygame

from gameutils.ecs.component import Component

class SolidGround(Component):
    pass

class SolidGroundSettler(Component):
    pass

@dataclass
class Grounded(Component):
    supporting_sprite: pygame.sprite.Sprite
