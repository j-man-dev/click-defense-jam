import math
import random
from pgzero.builtins import Actor
# from pgzero.loaders import images, sounds  # Manually import the magic loaders

from pygame import mask, transform
import pygame

# Global constants
# nested dictionary containing enemy images in different colors
ENEMY_ASSETS = {
    "black": {"image": "enemy_black", "path": "images/enemy_black.png"},
    "blue": {"image": "enemy_blue", "path": "images/enemy_blue.png"},
    "green": {"image": "enemy_green", "path": "images/enemy_green.png"},
    "orange": {"image": "enemy_orange", "path": "images/enemy_orange.png"},
    "pink": {"image": "enemy_pink", "path": "images/enemy_pink.png"},
    "purple": {"image": "enemy_purple", "path": "images/enemy_purple.png"},
    "red": {"image": "enemy_red", "path": "images/enemy_red.png"},
    "teal": {"image": "enemy_teal", "path": "images/enemy_teal.png"},
    "yellow": {"image": "enemy_yellow", "path": "images/enemy_yellow.png"},
}

# TODO 2: create a global dictionary of all player images
PLAYER_ASSETS = {
    "angry": {"image": "cat_angry", "path": "images/cat_angry.png"},
    "sad": {"image": "cat_sad", "path": "images/cat_sad.png"},
    "happy": {"image": "cat_happy", "path": "images/cat_happy.png"},
    "neutral": {"image": "cat_neutral", "path": "images/cat_neutral.png"},
    "meow": {"image": "cat_meow", "path": "images/cat_meow.png"},
}


# NOTE: ENTITIES module focus on WHAT it is and HOW to draw and move itself.
class Enemy(Actor):  # inherits Actor class to access its methods/prop
    """Docstring for Enemy
    Moves and rotates enemy to face target.
    Handles enemy spawn positions, movement toward target.
    """

    def __init__(self, image, image_path, speed, screen_width, screen_height):
        """
        Docstring for __init__


        """
        """Calls parent Actor constructor w/ passed image.png file
            Defines the random position of the enemy

        Args:
            image (str): the name of the image to create an Actor obj
            image_path(str): path of image.png MUST include file extension. (e.g. "images/myimage.png")
            screen_width (int): horizontal size of game screen in pixels
            screen_height (int): vertical size of game screen in pixels

        Attributes:
            self.speed (int): defines speed (px/sec) of the enemy
            self.spawn_pos() (tuple): (int, int) x, y spawn position coordinates
            self.mask (obj): current mask obj of rotated Surface. Updates dynamically
            self.mask_rect (obj): current mask rect ob of rotated Surface. Updates dynamically

        """

        super().__init__(image)  # creates Actor obj
        self.image_path = image_path
        self.speed = speed  # px/sec
        self.spawn_pos(
            screen_width, screen_height
        )  # sets spawn pos relative to screen dimensions
        self.image_surf = pygame.image.load(self.image_path)
        self.mask = None
        self.mask_rect = None

    # TODO 14: refactor: Move spawn pos logic to GameState class
    ## it tells WHERE to draw entities
    def spawn_pos(self, screen_width, screen_height):
        """Spawn from edges and corners off-screen."""
        sprite_diag = math.hypot(self.width, self.height)  # diagonal length
        buffer = int(sprite_diag * 0.5) + 50  # half diag + padding

        positions = {
            "left": (-buffer, "y"),
            "right": (screen_width + buffer, "y"),
            "top": ("x", -buffer),
            "bottom": ("x", screen_height + buffer),
            "top-left": (-buffer, -buffer),
            "top-right": (screen_width + buffer, -buffer),
            "bottom-left": (-buffer, screen_height + buffer),
            "bottom-right": (screen_width + buffer, screen_height + buffer),
        }

        # Choose random key value from positions dict
        side = random.choice(list(positions.keys()))

        pos_x, pos_y = positions[side]  # calls key value (x, y)

        # set Actor pos - syntax: Actor.x, Actor.y
        if pos_x == "x":  # top or bottom edge
            self.x = random.randint(buffer, screen_width - buffer)
            self.y = pos_y
        elif pos_y == "y":  # left or right edge
            self.y = random.randint(buffer, screen_height - buffer)
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

        # Rotate angle to face target - syntax: Actor.angle()
        self.angle = self.angle_to(target)  # ANTICLOCKWISE rotation

        # Create rotated surface & mask matching Actor's surf (CW to counter Actor's CCW)
        rotated_surf = transform.rotate(self.image_surf, -self.angle)
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
    def __init__(self, image, image_path, screen_width, screen_height):
        """Calls parent Actor constructor w/ input enemy.png
            Defines the random position of the enemy
        Args:
            image (str): the name of the image to create an Actor obj
            image_path(str): path of image.png MUST include file extension. (e.g. "images/myimage.png")
            screen_width (int): horizontal size of game screen in pixels
            screen_height (int): vertical size of game screen in pixels

        Attributes:
            self.pos (int): defines target x and y position by its center
            self.mask (obj): mask object of the loaded target.png
            self.mask_rect (obj): Rect obj of the mask obj after center matches target.pos center
        """
        super().__init__(image)  # create Actor obj
        self.image_path = image_path
        self.pos = screen_width // 2, screen_height // 2
        self.image_surf = pygame.image.load(self.image_path)
        self.mask = mask.from_surface(self.image_surf)
        self.mask_rect = self.mask.get_rect(center=(self.x, self.y))


# TODO 1: Add ability to change the value of 'image_path' after obj created
## create attributes to store'image_path' so it can be accessed/edited in code


class Player:
    def __init__(self, image_path):
        """Creates a player sprite as the mouse cursor.

        Args:
            image (str): the name of the image to create an Actor obj
            image_path(str): path of image.png MUST include file extension. (e.g. "images/myimage.png")

        """
        self.image_path = image_path

        # -- Create Rect obj hitbox from image_path of image-- #
        self.image_surf = pygame.image.load(self.image_path).convert_alpha()
        # Rect obj created once at __init__ instead of multiple times in draw() loop
        self.rect = self.image_surf.get_rect()

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()  # retrieves mouse pos
        # by default image top-left Rect hitbox stick to mouse, we want it to align center
        # Sync hitbox center to mouse pos using Rect .center property
        self.rect.center = (mouse_x, mouse_y)

        # draw player image at mouse pos.
        screen.blit(self.image_surf, self.rect)
