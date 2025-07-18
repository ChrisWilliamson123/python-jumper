from dataclasses import dataclass
from gameutils.ecs.component import Component

@dataclass
class Mass(Component):
    value: float # in Kg
