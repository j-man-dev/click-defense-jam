import math
import random  # random module to access pseudo-random numbers
import pgzrun
from pygame import mask, transform
from typing import TYPE_CHECKING, Any

# Avoid Pylance 'not defined' warnings for Pygame Zero objects
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

    # Below are classes/methods.
    class Actor:
        pass


# Screen resolution 1280x720
WIDTH = 1280  # constant variable for horizontal size
HEIGHT = 720  # constant variable for vertical size


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
        sprite_diag = math.hypot(self.width, self.height)  # diagonal length
        buffer = int(sprite_diag * 0.5) + 50  # half diag + padding

        positions = {
            "left": (-buffer, "y"),
            "right": (WIDTH + buffer, "y"),
            "top": ("x", -buffer),
            "bottom": ("x", HEIGHT + buffer),
            "top-left": (-buffer, -buffer),
            "top-right": (WIDTH + buffer, -buffer),
            "bottom-left": (-buffer, HEIGHT + buffer),
            "bottom-right": (WIDTH + buffer, HEIGHT + buffer),
        }

        # Choose random key value from positions dict
        side = random.choice(list(positions.keys()))

        pos_x, pos_y = positions[side]  # calls key value (x, y)

        if pos_x == "x":  # top or bottom edge
            self.x = random.randint(buffer, WIDTH - buffer)
            self.y = pos_y
        elif pos_y == "y":  # left or right edge
            self.y = random.randint(buffer, HEIGHT - buffer)
            self.x = pos_x
        else:  # corners
            self.x, self.y = pos_x, pos_y

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
    """update() loop called automatically by Pygame Zero 60x/sec.
    It handles game logic: spawn rate, movement, collisions, scoring.

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


def on_mouse_down(pos, button):
    """Remove enemies at mouse click pos

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


# start pygame zero game loop using Python interpreter to run
pgzrun.go()
