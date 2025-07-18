import pygame

from gameutils.ecs.world import World
from gameutils.sprites.sprite_sheet import SpriteSheet
from gameutils.sprites.sprite import Sprite as SpriteModel

from components.earth import Earth
from components.gravity import Gravity
from components.mass import Mass
from components.player import Player
from components.player_controlled import PlayerControlled
from components.position import Position
from components.screen_bounded import ScreenBounded
from components.screen_wrapped import ScreenWrapped
from components.solid_ground import SolidGround, SolidGroundSettler
from components.sprite import Sprite
from components.velocity import Velocity
from models.screen_edge import ScreenEdge
from settings.jumper_settings import JumperSettings
from sprites.image_sprite import ImageSprite
from sprites.player_sprite import PlayerSprite
from systems.platform_generation_system import PlatformGenerationSystem
from systems.collision_system import CollisionSystem
from systems.gravity_system import GravitySystem
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.render_system import RenderSystem
from systems.screen_bounding_system import ScreenBoundingSystem
from systems.screen_wrapping_system import ScreenWrappingSystem
from systems.scroll_system import ScrollSystem
from systems.solid_ground_system import SolidGroundSystem
from systems.sprite_destruction_system import SpriteDestructionSystem
from systems.sprite_rect_generation_system import SpriteRectGenerationSystem

# Game setup
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = SCREEN_WIDTH // (16 / 9)
EARTH_MASS_MULTIPLIER = 50

def create_player(world, width, height, x, y, color):
    player_sprite = PlayerSprite(width=width, height=height, color=color)
    player = world.create_entity()
    player.add_component(Position(x, y))
    player.add_component(Sprite(player_sprite))
    player.add_component(Gravity())
    player.add_component(Mass(1))
    player.add_component(Velocity(0, 0))
    player.add_component(PlayerControlled())
    player.add_component(Player())
    player.add_component(ScreenBounded([ScreenEdge.BOTTOM]))
    player.add_component(ScreenWrapped([ScreenEdge.RIGHT, ScreenEdge.LEFT]))
    player.add_component(SolidGroundSettler())

def __main__():
    settings = JumperSettings()
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Jumper')
    world = World()
    world.running = True

    # Player Entity
    create_player(world, 20, 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 'red')

    # Earth Entity
    earth = world.create_entity()
    earth.add_component(Position(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT + (6.378 * (10**6)))) # Center of the earth
    earth.add_component(Gravity())
    earth.add_component(Mass(5.972 * (10**24) * EARTH_MASS_MULTIPLIER))
    earth.add_component(Earth())

    # Platform
    terrain_sprites = [
        SpriteModel('platform', (272, 0), (58, 5))
    ]
    terrain_sprite_sheet = SpriteSheet('assets/sprite_sheets/terrain.png', terrain_sprites)
    terrain_sprites = terrain_sprite_sheet.get_sprites()

    # for i in range(0, 10):
    #     platform = world.create_entity()
    #     platform.add_component(Sprite(ImageSprite(terrain_sprites['platform'])))
    #     platform.add_component(Position(100 + (i * 50), SCREEN_HEIGHT - 5 - (i * 80)))
    #     platform.add_component(SolidGround())

    # Setting up sprite groups
    solid_ground_settler_sprite_group = pygame.sprite.Group()
    for (_, (sprite, _)) in world.get_entities_with_components(Sprite, SolidGroundSettler):
        solid_ground_settler_sprite_group.add(sprite.sprite)

    solid_ground_sprite_group = pygame.sprite.Group()
    for (_, (sprite, _)) in world.get_entities_with_components(Sprite, SolidGround):
        solid_ground_sprite_group.add(sprite.sprite)

    # Systems
    input_system = InputSystem(settings)
    gravity_system = GravitySystem()
    collision_system = CollisionSystem(solid_ground_sprite_group)
    movement_system = MovementSystem()
    platform_generation_system = PlatformGenerationSystem(SCREEN_WIDTH, SCREEN_HEIGHT, terrain_sprites, solid_ground_sprite_group)
    sprite_rect_generation_system = SpriteRectGenerationSystem()
    solid_ground_system = SolidGroundSystem(solid_ground_sprite_group, solid_ground_settler_sprite_group)
    screen_bounding_system = ScreenBoundingSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    screen_wrapping_system = ScreenWrappingSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    scroll_system = ScrollSystem(settings)
    sprite_destruction_system = SpriteDestructionSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    render_system = RenderSystem(screen)
    systems = [
        input_system,
        gravity_system,
        collision_system,
        movement_system,
        platform_generation_system,
        sprite_rect_generation_system,
        solid_ground_system,
        scroll_system,
        screen_bounding_system,
        screen_wrapping_system,
        sprite_destruction_system,
        render_system
    ]
    for system in systems:
        world.add_system(system)

    while world.running:
        dt = clock.tick(settings.framerate) / 1000.0

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                world.running = False

        screen.fill(pygame.Color("black"))
        world.update(dt)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    __main__()    
