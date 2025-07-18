from gameutils.ecs.system import System

from components.position import Position
from components.sprite import Sprite

class SpriteRectGenerationSystem(System):
    def update(self, dt):
        for (_, (sprite, position)) in self.world.get_entities_with_components(Sprite, Position):
            # Update the sprite's rect position
            sprite.sprite.rect.centerx = position.x
            sprite.sprite.rect.centery = position.y
