# TODO 0: import pgzrun and add pgzrun.go() at end of code

import random  # random module to access pseudo-random numbers
import pgzrun
from typing import TYPE_CHECKING, Any

# To avoid Pylance 'not defined' warnings for Pygame Zero objects
if TYPE_CHECKING:
    # If type checking is being performed, the following variables are assumed to exist and may be of any type.
    screen: Any
    keyboard: Any
    mouse: Any
    images: Any
    sounds: Any
    music: Any
    clock: Any

    # Below are classes. Pretend the class exists
    class Actor:
        pass


# TODO 1: Create a window screen
## Screen resolution 1280x720
WIDTH = 1280  # constant variable for horizontal size
HEIGHT = 720  # constant variable for vertical size

# TODO 2: Enemy spawn
# TODO 2.1: Create an Enemy class that defines what it has and does
## inherit Actor class: access methods/prop that handle moving sprites/graphics
## initialize parent Actor with enemy.png
## Define attributes (has): speed, position, image
## Define methods (does):
### random edge spawn using Actor prop left, right, top, bottom, x, y


class Enemy(Actor):  # inherits Actor class to access its methods/prop
    """Docstring for Enemy
    Moving enemy that spawns from edges and chases the target.
    Handles enemy spawning, movement toward target, and collision detection
    """

    def __init__(self):  # requires enemy image
        # Needs images/enemy.png
        super().__init__("enemy")  # calls parent Actor constructor
        self.speed = 10  # 10px/sec
        self.spawn_pos()  # calls the spawn_pos() method

    def spawn_pos(self):
        """Spawn from left/right/top/bottom screen edge.
        Visible for now but need to be off-screen later."""
        side = random.choice(["left", "right", "top", "bottom"])

        if side == "left":
            self.left = 0  # set enemy left-hand side pos @ left edge
            self.y = random.randint(0, HEIGHT)  # y pos rand int b/w 0 & HEIGHT
        elif side == "right":
            self.right = WIDTH  # set enemy right-hand side @ right edge
            self.y = random.randint(0, HEIGHT)
        elif side == "top":
            self.top = 0  # set enemy top-side @ top edge
            self.x = random.randint(0, WIDTH)  # x pos rand int b/w 0 & WIDTH
        else:
            self.bottom = 0  # set enemy bottom-hand side @ bottom edge
            self.x = random.randint(0, WIDTH)


# # Debug 1: Draw the enemy check that it is painted on screen

# enemy = Enemy()  # create Enemy obj -> Actor


# def draw():  # paint on screen
#     enemy.draw()


# TODO 2.2: Spawn multiple enemies at an interval
## Create a game state class that holds all the game data variables together:
### zero enemies, score, and spawn timer. spawn interval 2 sec
## Use the udpate() function to create new enemy based on spawn interval
### def update(dt) -> dt = time since last frame given automatically by Pygame Zero
### if 2 seconds passed since last spawn, add new Enemy obj to the Gamestate enemies list
## Create a draw() func to paint on screen
### draw the enemy spawn


class GameState:
    def __init__(self):
        """Holds all the game start data variables together.

        Attributes:
            self.enemies (list): Empty list to store Enemy Actor objects. 0 enemies at start
            self.spawn_timer (int): timer counting in secs since last spawn. Starts at 0.
            self.spawn_interval (int): Define how often enemy spawn.
            self.score (int): tracks player's score. Start at 0
        """
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.score = 0


game = GameState()  # creates instance of GameState class


def update(dt):
    """update() is called automatically by Pygame Zero 60x/sec.
    It handles spawn rate, movement, collisions, scoring.

    Args:
        dt (float): delta time is time since last frame. Given automatically by Pygame Zero
    """

    # Enemy spawn rate
    game.spawn_timer += dt  # spawn timer increases every frame by dt value

    if game.spawn_timer > game.spawn_interval:
        game.enemies.append(
            Enemy()
        )  # New Enemy obj created and appended to enemies list
        game.spawn_timer = 0  # reset spawn timer after new enemy spawns
        # # Debug 2: test that enemies list is updated by printing
        # print(game.enemies)


def draw():
    """draw() automatically by Pygame Zero when it needs to redraw your game window.
    It handles painting the enemy and target on the screen
    """
    screen.clear()  # erases old drawings when draw() is called
    for enemy in (
        game.enemies
    ):  # iterate for every item in game.enemies list, temp store in enemy var
        enemy.draw()  # draw Enemy obj each iteration


pgzrun.go()  # starts pygame zero game loop. can use Python interpreter to run
