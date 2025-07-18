import random
import pygame

from gameutils.ecs.system import System

from components.position import Position
from components.sprite import Sprite
from components.solid_ground import SolidGround
from sprites.image_sprite import ImageSprite

class PlatformGenerationSystem(System):
    def __init__(self, screen_width, screen_height, terrain_sprites, solid_ground_group):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.terrain_sprites = terrain_sprites
        self.solid_ground_group = solid_ground_group
        self.platform_count = 0
        self.last_platform_pos = None

        # Player jump physics (approximate)
        self.jump_velocity = -300
        self.gravity = 9.8 * 50 # From your gravity system
        self.player_x_speed = 200

        # Time to reach max jump height
        time_to_peak = -self.jump_velocity / self.gravity
        # Max jump height
        self.max_jump_height = self.jump_velocity * time_to_peak + 0.5 * self.gravity * time_to_peak**2
        # Horizontal distance covered during jump
        self.max_horizontal_distance = self.player_x_speed * (2 * time_to_peak)

    def update(self, dt):
        platform_count = len(self.world.get_entities_with_components(SolidGround))
        to_gen = 10 - platform_count
        for _ in range(to_gen):
            self.generate_platform()

    def generate_platform(self):
        platform_choice = random.choice(['platform1', 'platform2', 'platform3'])
        platform_sprite_model = self.terrain_sprites[platform_choice]
        platform_width = platform_sprite_model.get_width()
        platform_height = platform_sprite_model.get_height()

        if self.last_platform_pos is None:
            # First platform
            x = self.screen_width / 2
            y = self.screen_height - platform_height - 50
        else:
            # Subsequent platforms
            # Ensure the next platform is reachable
            max_y_diff = self.max_jump_height * 0.8 # 80% of max jump height for safety
            max_x_diff = self.max_horizontal_distance * 0.8

            y_offset = random.uniform(-max_y_diff * 0.5, -max_y_diff)
            x_offset = random.uniform(-max_x_diff, max_x_diff)

            new_x = self.last_platform_pos.x + x_offset
            new_y = self.last_platform_pos.y - y_offset

            # Clamp to screen bounds
            x = max(platform_width / 2, min(new_x, self.screen_width - platform_width / 2))
            y = max(platform_height / 2, min(new_y, self.screen_height - platform_height / 2))

        platform = self.world.create_entity()
        sprite = ImageSprite(platform_sprite_model)
        platform.add_component(Sprite(sprite))
        pos_comp = Position(x, y)
        platform.add_component(Position(x, y))
        platform.add_component(SolidGround())

        self.solid_ground_group.add(sprite)

        self.last_platform_pos = pos_comp
