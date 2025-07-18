from gameutils.ecs.system import System

from components.position import Position
from components.screen_wrapped import ScreenWrapped
from components.sprite import Sprite
from models.screen_edge import ScreenEdge

class ScreenWrappingSystem(System):
    """Wraps ScreenWrapped entities around the screen's edges"""
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, dt):
        # If the object is fully off screen, wrap it
        for (_, (position, sprite, screen_wrapped)) in self.world.get_entities_with_components(Position, Sprite, ScreenWrapped):
            width = sprite.sprite.rect.width
            height = sprite.sprite.rect.height
            if ScreenEdge.RIGHT in screen_wrapped.edges:
                if sprite.sprite.rect.x > self.screen_width:
                    position.x = -(width // 2)

            if ScreenEdge.LEFT in screen_wrapped.edges:
                if sprite.sprite.rect.x < -width:
                    position.x = self.screen_width - (width // 2)
