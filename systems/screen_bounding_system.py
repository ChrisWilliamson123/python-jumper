from gameutils.ecs.system import System

from components.position import Position
from components.screen_bounded import ScreenBounded
from components.solid_ground import Grounded, SolidGroundSettler
from components.sprite import Sprite
from components.velocity import Velocity
from models.screen_edge import ScreenEdge

class ScreenBoundingSystem(System):
    """Binds ScreenBounded entities to the screen's bounds"""
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt):
        for (entity, (position, velocity, sprite, screen_bounded)) in self.world.get_entities_with_components(Position, Velocity, Sprite, ScreenBounded):
            if ScreenEdge.BOTTOM in screen_bounded.edges:
                height = sprite.sprite.rect.height
                bottom = position.y + (height // 2)
                if bottom >= self.screen_height:
                    position.y = self.screen_height - (height // 2)
                    velocity.y = 0

                    if entity.get_component(SolidGroundSettler):
                        entity.add_component(Grounded(None))
