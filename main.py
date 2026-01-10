# TODO 0: import pgzrun and add pgzrun.go() at end of code

import math
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
## Define attributes (has): speed, position
## Define methods (does):
### random edge spawn using Actor prop left, right, top, bottom, x, y
# TODO 2.4: Make enemy spawn face the target
## Create a update() function inside Enemy class
### set enemy angle to face target Actor center
###  Actor.angle = Actor.angle_to(target) method
## call enemy udpate() in global udpate() to update the enemy spawn angle
# TODO 3: Enemy Movement
# TODO 3.1: Make enemy move towards the target
## Update Enemy class update() method with input dt (delta time)
## Calculate velocity vector = unit direction vector * scalar speed * dt
### unit vector direction =  distance vector / distance magnitude
### scalar speed = number (unit: px/sec)
### dt = time since last frame (0.016 @ 60fps). Given automatically by Pygame Zero


class Enemy(Actor):  # inherits Actor class to access its methods/prop
    """Docstring for Enemy
    Moving enemy that spawns from edges and chases the target.
    Handles enemy spawning, movement toward target, and collision detection
    """

    def __init__(self):
        """Calls parent Actor constructor w/ input enemy.png
            Defines the random position of the enemy

        Attributes:
            self.speed (int): defines speed (px/sec) of the enemy
        """
        super().__init__("enemy")  # needs image.png
        self.speed = 20  # 10px/sec
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
            self.bottom = HEIGHT  # set enemy bottom-hand side @ bottom edge
            self.x = random.randint(0, WIDTH)

    def update(self, target, dt):
        """Moves and rotates its right side to the target's center.

        Args:
            target (obj): The Actor object of our target
        """

        # Rotate RIGHT side to face target
        self.angle = self.angle_to(target)

        # Move toward target center
        # NOTE: velocity vector = unit direction vector * speed * dt
        ## distance vector
        dx = target.x - self.x
        dy = target.y - self.y
        ## distance magnitude
        dist = math.sqrt(dx**2 + dy**2)
        ## Velocity vector (direction and speed)
        if dist > 5:  # prevents division by 0 error
            self.x += dx / dist * self.speed * dt
            self.y += dy / dist * self.speed * dt


# # Debug 1: Draw the enemy check that it is painted on screen

# enemy = Enemy()  # create Enemy obj -> Actor


# def draw():  # paint on screen
#     enemy.draw()

# TODO 2.3: Create a class for the target that defines what is has and does
## inherit Actor class: access methods/prop that handle moving sprites/graphics
## initialize parent Actor with target.png
## Define attributes (has): position


class Target(Actor):
    def __init__(self):
        """Calls parent Actor constructor w/ input enemy.png
            Defines the random position of the enemy

        Attributes:
            self.pos (int): defines target x and y position by its center
        """
        super().__init__("target")  # Needs image.png
        self.pos = WIDTH // 2, HEIGHT // 2


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
target = Target()  # creates instance of Target class (Actor obj)


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
        # for enemy in game.enemies:  # iterate through game.enemies Enemy obj list
        #     enemy.update(target=target)  # update enemy angle to face target center
        game.spawn_timer = 0  # reset spawn timer after new enemy spawns
    for enemy in game.enemies:  # iterate through game.enemies Enemy obj list
        enemy.update(target, dt)  # update enemy angle to face target center
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
    target.draw()  # draw Target obj


pgzrun.go()  # starts pygame zero game loop. can use Python interpreter to run
