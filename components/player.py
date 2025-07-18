from dataclasses import dataclass
from gameutils.ecs.component import Component

from models.direction import Direction

@dataclass
class Player(Component):
    facing_direction: Direction = Direction.RIGHT
