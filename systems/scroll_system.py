from gameutils.ecs.system import System

from components.position import Position

class ScrollSystem(System):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    """Moves anything with a position downwards"""
    def update(self, dt):
        for (_, (components)) in self.world.get_entities_with_components(Position):
            position = components[0]
            position.y += self.settings.scroll_speed * dt
