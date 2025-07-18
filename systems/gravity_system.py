from gameutils.ecs.system import System

from components.earth import Earth
from components.gravity import Gravity
from components.mass import Mass
from components.position import Position
from components.solid_ground import Grounded
from components.velocity import Velocity

class GravitySystem(System):
    """Pulls all components with gravity towards a single Earth component"""
    def update(self, dt):
        (earth, _) = self.world.get_entity_with_singular_component(Earth)
        earth_position = earth.get_component(Position)
        earth_mass = earth.get_component(Mass)
        earth_gravity = earth.get_component(Gravity)
        
        for (entity, (position, mass, _, velocity)) in self.world.get_entities_with_components(Position, Mass, Gravity, Velocity):
            if entity.get_component(Earth) or entity.get_component(Grounded):
                velocity.y = 0
                continue

            delta_y = abs(earth_position.y - position.y)
            gravitational_force = self._gravitational_force(earth_gravity.constant, earth_mass.value, mass.value, delta_y)
            acceleration = gravitational_force / mass.value

            if earth_position.y < position.y:
                acceleration *= -1

            velocity.y += (acceleration * dt)

    def _gravitational_force(self, g, m1, m2, d):
        """g: (m3⋅kg−1⋅s−2), m: (Kg), d: (m)"""
        f = (g * m1 * m2) / (d ** 2)
        return f
