from gameutils.ecs.system import System

from components.position import Position
from components.velocity import Velocity

class MovementSystem(System):
    """Adjusts the position of all components with velocity"""
    def update(self, dt):
        for (_, (position, velocity)) in self.world.get_entities_with_components(Position, Velocity):
            position.x += (velocity.x * dt)
            position.y += (velocity.y * dt)
