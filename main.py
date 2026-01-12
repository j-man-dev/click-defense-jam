# TODO 0: import pgzrun and add pgzrun.go() at end of code

import math
import random  # random module to access pseudo-random numbers
import pgzrun
from pygame import mask, transform
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
    anchor: Any

    # Below are classes/methods. Pretend the class exists
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
# TODO 3.2: Make enemy start off-screen
## adjust x, y pos in def spawn_pos() to set enemy off-screen


class Enemy(Actor):  # inherits Actor class to access its methods/prop
    """Docstring for Enemy
    Moves and rotates enemy to face target.
    Handles enemy spawning, movement toward target.
    """

    def __init__(self):
        """Calls parent Actor constructor w/ input enemy.png
            Defines the random position of the enemy

        Attributes:
            self.speed (int): defines speed (px/sec) of the enemy
            self.orig_surf (obj): original Surface of loaded enemy.png
            self.spawn_pos() (tuple): (int, int) x, y spawn position coordinates
            self.mask (obj): current mask obj of rotated Surface. Updates dynamically
            self.anchor (str): defines reference point for position
        """

        super().__init__("enemy")  # needs image.png
        self.speed = 80  # px/sec
        self.spawn_pos()  # calls the spawn_pos() method
        self.orig_surf = images.enemy
        self.mask = None
        self.anchor = "center", "center"  # explicit (default)

    def spawn_pos(self):
        """Spawn from edges and corners off-screen."""
        side = random.choice(["left", "right", "top", "bottom"])
        sprite_diag = math.hypot(self.width, self.height)  # diagonal length
        sprite_buffer = int(sprite_diag * 0.5) + 50  # half diag + padding

        if side == "left":
            self.x = -sprite_buffer  # set enemy head pos left off-screen
            self.y = random.randint(0, HEIGHT)  # y pos rand int b/w 0 & HEIGHT
        elif side == "right":
            self.x = WIDTH + sprite_buffer  # set enemy head right off-screen
            self.y = random.randint(0, HEIGHT)
        elif side == "top":
            self.y = -sprite_buffer  # set enemy head top off-screen
            self.x = random.randint(0, WIDTH)  # x pos rand int b/w 0 & WIDTH
        else:
            self.y = HEIGHT + sprite_buffer  # set enemy head bottom off-screen
            self.x = random.randint(0, WIDTH)

    def update(self, target, dt):
        """Moves and rotates its right side to the target's center.
        Stores rotated offset for mask alignment to Actor's draw.

        Args:
            target (obj): The Actor object of our target

        Attributes:
            self.angle (float): updates the Actor visual angle. rotates counter-clockwise
            self.mask_rect (obj): Rect obj of the mask obj after rotation and center aligns with enemy.pos center
        """

        # Rotate angle to face target
        self.angle = self.angle_to(target)  # ANTICLOCKWISE rotation

        # Create rotated surface & mask matching Actor's draw (CW to counter Actor's CCW)
        rotated_surf = transform.rotate(self.orig_surf, -self.angle)
        self.mask = mask.from_surface(rotated_surf)  # mask of rotated surface

        # Create rotated mask Rect obj center to match enemy.pos
        self.mask_rect = self.mask.get_rect(center=(self.x, self.y))

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
            self.mask (obj): mask object of the loaded target.png
            self.mask_rect (obj): Rect obj of the mask obj after center matches target.pos center
        """
        super().__init__("target")  # Needs image.png
        self.pos = WIDTH // 2, HEIGHT // 2
        self.mask = mask.from_surface(images.target)
        self.mask_rect = self.mask.get_rect(center=(self.x, self.y))


# TODO 2.2: Spawn multiple enemies at an interval
## Create a game state class that holds all the game data variables together:
### zero enemies, score, and spawn timer. spawn interval 2 sec
## Use the udpate() function to create new enemy based on spawn interval
### def update(dt) -> dt = time since last frame given automatically by Pygame Zero
### if 2 seconds passed since last spawn, add new Enemy obj to the Gamestate enemies list
## Create a draw() func to draw enemy spawn

# TODO 6: Loss condition
# TODO 6.1: End game when enemy reaches the target
## in GameState class, add game_over boolean flag to signal ON/OFF game state
## in global update() loop game logic: check if collision b/w enemy & target is True
### Use pixel-perfect collision detection: mask.overlap()
### stop/pause the game if True


class GameState:
    def __init__(self):
        """Holds all the game state data variables together (menu, play, end).

        Attributes:
            self.enemies (list): Store list of Enemy Actor objects. 0 enemies at start
            self.spawn_timer (int): timer counting in secs since last spawn. Starts at 0.
            self.spawn_interval (int): Define how often enemy spawn.
            self.score (int): tracks player's score. Start at 0
            self.game_over (bool): Boolean flag set to False to signal game is not over
        """
        # Current screen/mode (menu, playing, game_over)

        # Gameplay data
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.score = 0

        # Menu data

        # Game over data
        self.game_over = False


# Create instance obj
game = GameState()  # creates instance of GameState class
target = Target()  # creates instance of Target class (Actor obj)


def update(dt):
    """update() is called automatically by Pygame Zero 60x/sec.
    It handles spawn rate, movement, collisions, scoring.

    Args:
        dt (float): delta time is time since last frame. Given automatically by Pygame Zero
    """

    if game.game_over:  # is game_over True?
        return  # Exit out of def update() game loop/freezes screen

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

        # PIXEL-PERFECT COLLISIOIN DETECTION
        dx = int(enemy.mask_rect.left - target.mask_rect.left)  # left offset pos
        dy = int(enemy.mask_rect.top - target.mask_rect.top)  # top offset pos
        collision_point = target.mask.overlap(enemy.mask, (dx, dy))
        if collision_point:  # opaque pixels touch?
            game.game_over = True  # opaque pixels touched -> pause game
            print("GAME OVER!")


# TODO 4: Player interaction
# TODO 4.1: Create function that removes enemy when clicked
## use automatically called on_mouse_down(pos, button) func.
## check if input button is left mouse click and input pos collides with enemy
### Actor_obj.collidepoint(pos)
## remove enemy from enemies list -> list.remove(element)
# TODO 5: Increase score by every time an enemy is removed
## update game.score attribute value with score accumulation


def on_mouse_down(pos, button):
    """Remove enemies at mouse pos

    Args:
        pos (tuple): (x, y) tuple that gives location of mouse pointer when button pressed.
        button (obj): A mouse enum value indicating the button that was pressed.
    """
    for enemy in game.enemies:
        if button == mouse.LEFT and enemy.collidepoint(pos):
            game.enemies.remove(enemy)
            game.score += 1
            # # DEBUG start: test that the score accumulate when enemy is removed
            # print(game.score)
            # # DEBUG end: test that the score accumulate when enemy is removed


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
