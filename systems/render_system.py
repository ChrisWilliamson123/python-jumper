import pygame

from gameutils.ecs.system import System

from components.position import Position
from components.sprite import Sprite

class RenderSystem(System):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.sprite_group = pygame.sprite.Group()

    def update(self, dt):
        self.sprite_group.empty()

        for (_, (sprite, position)) in self.world.get_entities_with_components(Sprite, Position):
            # Update the sprite's rect position
            sprite.sprite.rect.centerx = position.x
            sprite.sprite.rect.centery = position.y

            self.sprite_group.add(sprite.sprite)

        self.sprite_group.draw(self.screen)
