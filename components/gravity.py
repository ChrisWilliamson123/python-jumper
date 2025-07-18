from dataclasses import dataclass
from gameutils.ecs.component import Component

@dataclass
class Gravity(Component):
    constant: float = 6.673 * (10**-11)
