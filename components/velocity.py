from dataclasses import dataclass
from gameutils.ecs.component import Component

@dataclass
class Velocity(Component):
    x: float = 0.0
    y: float = 0.0
