import pygame

from gameutils.ecs.system import System

from components.facing_direction import FacingDirection
from components.player import Player
from components.player_controlled import PlayerControlled
from components.solid_ground import Grounded
from components.velocity import Velocity
from models.direction import Direction

class InputSystem(System):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def update(self, dt):
        keys_pressed = pygame.key.get_pressed()
        
        for (entity, (_, _, velocity, facing)) in self.world.get_entities_with_components(Player, PlayerControlled, Velocity, FacingDirection):
            # Can only jump if our y velocity is zero (i.e. we have something underneath us)
            # TODO: This could break when we get to the top of the jump and velocity hits zero?
            jump_key = pygame.K_SPACE
            if keys_pressed[jump_key] and entity.get_component(Grounded):
                velocity.y = -300
                entity.remove_component(Grounded)

            left_key = pygame.K_LEFT
            right_key = pygame.K_RIGHT
            new_x_vel = 0
            # Horizontal movement
            if keys_pressed[left_key]:
                new_x_vel -= self.settings.player_x_speed
                facing.direction = Direction.LEFT
            if keys_pressed[right_key]:
                new_x_vel += self.settings.player_x_speed
                facing.direction = Direction.RIGHT

            velocity.x = new_x_vel
