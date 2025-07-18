import pygame

from gameutils.ecs.system import System

from components.position import Position
from components.velocity import Velocity
from components.sprite import Sprite
from components.solid_ground import SolidGround, SolidGroundSettler, Grounded

class CollisionSystem(System):
    def __init__(self, solid_ground_group):
        super().__init__()
        self.solid_ground_group = solid_ground_group

    def update(self, dt):
        for entity, (position, velocity, sprite, _) in self.world.get_entities_with_components(Position, Velocity, Sprite, SolidGroundSettler):
            if velocity.y <= 0:
                continue

            # Create a rect for the next frame's position
            next_y = position.y + (velocity.y * dt)
            next_x = position.x + (velocity.x * dt)
            next_rect = pygame.Rect(0, 0, sprite.sprite.rect.width, sprite.sprite.rect.height)
            next_rect.center = (next_x, next_y)
            bottom_rect = pygame.Rect(0, 0, sprite.sprite.rect.width, 10)
            bottom_rect.centerx = next_rect.centerx
            bottom_rect.centery = next_rect.bottom - 5

            for ground_sprite in self.solid_ground_group:
                if not ground_sprite.rect.colliderect(sprite.sprite.rect) and ground_sprite.rect.colliderect(bottom_rect):
                    # Collision detected
                    velocity.y = 0
                    position.y = ground_sprite.rect.top - ((sprite.sprite.rect.height // 2) - 1)
                    entity.add_component(Grounded(ground_sprite))
                    break # Stop checking after the first collision
            else:
                # No collision
                if entity.get_component(Grounded):
                    entity.remove_component(Grounded)
