from dataclasses import dataclass
from gameutils.ecs.component import Component

from models.direction import Direction

@dataclass
class FacingDirection(Component):
    direction: Direction = Direction.RIGHT
