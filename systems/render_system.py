import pygame

from gameutils.ecs.system import System

from components.sprite import Sprite

class RenderSystem(System):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.sprite_group = pygame.sprite.Group()

    def update(self, dt):
        self.sprite_group.empty()

        for (_, components) in self.world.get_entities_with_components(Sprite):
            self.sprite_group.add(components[0].sprite)

        self.sprite_group.draw(self.screen)
