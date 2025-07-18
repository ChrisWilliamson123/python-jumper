import pygame

from gameutils.ecs.component import Component
from gameutils.ecs.system import System

from gameutils.ecs.world import World

from components.earth import Earth
from components.gravity import Gravity
from components.mass import Mass
from components.player import Player
from components.player_controlled import PlayerControlled
from components.position import Position
from components.screen_bounded import ScreenBounded
from components.sprite import Sprite
from components.velocity import Velocity
from models.screen_edge import ScreenEdge
from sprites.sprite import PlayerSprite
from systems.gravity_system import GravitySystem
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.render_system import RenderSystem
from systems.screen_bounding_system import ScreenBoundingSystem

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

def __main__():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption('Jumper')
    world = World()
    world.running = True

    # Systems
    input_system = InputSystem()
    gravity_system = GravitySystem()
    movement_system = MovementSystem()
    screen_bounding_system = ScreenBoundingSystem(SCREEN_WIDTH, SCREEN_HEIGHT)
    render_system = RenderSystem(screen)
    systems = [
        input_system,
        gravity_system,
        movement_system,
        screen_bounding_system,
        render_system
    ]
    for system in systems:
        world.add_system(system)

    # Player Entity
    create_player(world, 20, 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50, 'red')

    # Earth Entity
    earth = world.create_entity()
    earth.add_component(Position(x=SCREEN_WIDTH // 2, y=SCREEN_HEIGHT + (6.378 * (10**6)))) # Center of the earth
    earth.add_component(Gravity())
    earth.add_component(Mass(5.972 * (10**24) * EARTH_MASS_MULTIPLIER))
    earth.add_component(Earth())

    while world.running:
        dt = clock.tick(60) / 1000.0

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
