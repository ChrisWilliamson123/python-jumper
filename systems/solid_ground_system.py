import pygame

from gameutils.ecs.system import System

from components.position import Position
from components.solid_ground import Grounded, SolidGroundSettler
from components.sprite import Sprite
from components.velocity import Velocity

class SolidGroundSystem(System):
    """Ensures that SolidGroundSettlers can settle on SolidGround"""
    def __init__(self, solid_ground_group, settlers_group):
        super().__init__()
        self.solid_ground_group = solid_ground_group
        self.settlers_group = settlers_group

    def update(self, dt):
        for (entity, (_, sprite, velocity, position)) in self.world.get_entities_with_components(SolidGroundSettler, Sprite, Velocity, Position):
            if grounded := entity.get_component(Grounded):
                if supporting_sprite := grounded.supporting_sprite:
                    grounded_sprite = sprite.sprite

                    if not supporting_sprite.rect.colliderect(grounded_sprite):
                        entity.remove_component(Grounded)
