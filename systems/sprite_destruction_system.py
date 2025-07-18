import pygame

from gameutils.ecs.system import System

from components.player import Player
from components.position import Position
from components.sprite import Sprite
from components.velocity import Velocity

class SpriteDestructionSystem(System):
    """Destroys sprites"""
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_rect = pygame.Rect(0, 0, screen_width, screen_height)

    def update(self, dt):
        entities_to_remove = []
        for (entity, (_, sprite)) in self.world.get_entities_with_components(Position, Sprite):
            if entity.get_component(Player):
                continue
            rect = sprite.sprite.rect
            if self._is_rect_outside_screen_rect(rect, self.screen_rect):
                entities_to_remove.append(entity)
                sprite.sprite.kill()

        self.world.remove_entities(entities_to_remove)

    # Alternative version that takes a screen rect instead of width/height
    def _is_rect_outside_screen_rect(self, rect, screen_rect):
        """
        Check if a pygame rect is fully outside the screen bounds using a screen rect.
        
        Args:
            rect: pygame.Rect object to check
            screen_rect: pygame.Rect representing the screen bounds (usually (0, 0, width, height))
        
        Returns:
            bool: True if the rect is completely outside screen bounds, False otherwise
        """
        return (rect.right < screen_rect.left or 
                rect.left > screen_rect.right or 
                rect.bottom < screen_rect.top or 
                rect.top > screen_rect.bottom)
