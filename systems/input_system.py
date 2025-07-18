import pygame

from gameutils.ecs.system import System

from components.player import Player
from components.player_controlled import PlayerControlled
from components.velocity import Velocity

class InputSystem(System):
    def update(self, dt):
        keys_pressed = pygame.key.get_pressed()
        
        for (_, (_, _, velocity)) in self.world.get_entities_with_components(Player, PlayerControlled, Velocity):
            # Can only jump if our y velocity is zero (i.e. we have something underneath us)
            # TODO: This could break when we get to the top of the jump and velocity hits zero?
            jump_key = pygame.K_SPACE
            if keys_pressed[jump_key] and velocity.y == 0:
                velocity.y = -300

            left_key = pygame.K_LEFT
            right_key = pygame.K_RIGHT
            new_x_vel = 0
            # Horizontal movement
            if keys_pressed[left_key]:
                new_x_vel -= 200
            if keys_pressed[right_key]:
                new_x_vel += 200

            velocity.x = new_x_vel
