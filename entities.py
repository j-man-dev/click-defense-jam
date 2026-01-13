import math
import random
from pgzero.builtins import Actor
from pgzero.loaders import images, sounds  # Manually import the magic loaders

from pygame import mask, transform


class Enemy(Actor):  # inherits Actor class to access its methods/prop
    """Docstring for Enemy
    Moves and rotates enemy to face target.
    Handles enemy spawning, movement toward target.
    """

    def __init__(self, image, screen_width, screen_height):
        """
        Docstring for __init__


        """
        """Calls parent Actor constructor w/ passed image.png file
            Defines the random position of the enemy

        Args:
            image (str): the name of the image to create an Actor obj
            screen_width (int): horizontal size of game screen in pixels
            screen_height (int): vertical size of game screen in pixels

        Attributes:
            self.speed (int): defines speed (px/sec) of the enemy
            self.orig_surf (obj): original Surface of loaded enemy.png
            self.spawn_pos() (tuple): (int, int) x, y spawn position coordinates
            self.mask (obj): current mask obj of rotated Surface. Updates dynamically
            self.anchor (str): defines reference point for position
        """

        super().__init__(
            image
        )  # Calls Actor class to create Actor obj from image param
        self.speed = 80  # px/sec
        self.spawn_pos(
            screen_width, screen_height
        )  # sets spawn pos relative to screen dimensions
        self.orig_surf = images.enemy
        self.mask = None
        self.anchor = "center", "center"  # explicit (default)

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
    def __init__(self, image, screen_width, screen_height):
        """Calls parent Actor constructor w/ input enemy.png
            Defines the random position of the enemy

        Attributes:
            self.pos (int): defines target x and y position by its center
            self.mask (obj): mask object of the loaded target.png
            self.mask_rect (obj): Rect obj of the mask obj after center matches target.pos center
        """
        super().__init__(
            image
        )  # Calls Actor class to create Actor obj from image param
        self.pos = screen_width // 2, screen_height // 2
        self.mask = mask.from_surface(images.target)
        self.mask_rect = self.mask.get_rect(center=(self.x, self.y))
