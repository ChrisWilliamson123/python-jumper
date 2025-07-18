from dataclasses import dataclass
from gameutils.ecs.component import Component

from models.screen_edge import ScreenEdge

@dataclass
class ScreenBounded(Component):
    edges: list[ScreenEdge]
