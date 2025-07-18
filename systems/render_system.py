import pygame

from gameutils.ecs.system import System

from components.facing_direction import FacingDirection
from components.sprite import Sprite
from models.direction import Direction
from sprites.animated_sprite import AnimatedSprite

class RenderSystem(System):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.sprite_group = pygame.sprite.Group()

    def update(self, dt):
        self.sprite_group.empty()

        for (entity, components) in self.world.get_entities_with_components(Sprite):
            sprite = components[0].sprite
            self.sprite_group.add(sprite)

            if isinstance(sprite, AnimatedSprite): # TODO: Use the update function on the sprites instead
                if facing := entity.get_component(FacingDirection):
                    sprite.flip_x = True if facing.direction == Direction.LEFT else False
                sprite.change_image(dt)

        self.sprite_group.draw(self.screen)
