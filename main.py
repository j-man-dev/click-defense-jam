import pgzrun
from typing import TYPE_CHECKING, Any

from game_state import GameState
from entities import Enemy, Target
from ui import Button

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
WIDTH = 1920  # constant variable for horizontal size
HEIGHT = 1080  # constant variable for vertical size

# Instances of classes
game = GameState()
target = Target(image="target", screen_width=WIDTH, screen_height=HEIGHT)


def update(dt):
    """update() loop called automatically by Pygame Zero 60x/sec.
    It handles game logic: spawn rate, movement, collisions, scoring,

    Args:
        dt (float): delta time is time since last frame. Given automatically by Pygame Zero
    """

    if game.game_over:  # is game_over True?
        return  # Exit out of def update() game loop/freezes screen

    # Enemy spawn rate
    game.spawn_timer += dt  # spawn timer increases every frame by dt value

    if game.spawn_timer > game.spawn_interval:
        enemy = Enemy(image="enemy", screen_width=WIDTH, screen_height=HEIGHT)
        game.enemies.append(enemy)  # New Enemy obj created and appended to enemies list
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
    """Remove enemies at mouse click pos. Called automatically by Pygame zero

    Args:
        pos (tuple): (x, y) tuple that gives location of mouse pointer when button pressed.
        button (obj): A mouse enum value indicating the button that was pressed.
    """
    for enemy in game.enemies:
        if button == mouse.LEFT and enemy.collidepoint(pos):
            game.enemies.remove(enemy)
            game.score += 1
            # Difficulty-scaling: Increase spawn freq every x points
            if (
                game.score % game.difficulty_score_interval == 0
            ):  # is score cleanly divisibly by score interval?
                game.spawn_interval = max(
                    0.2, game.spawn_interval * (1 - game.spawn_interval_decrease)
                )  # don't let spawn interval go below 0.2s

            # # DEBUG start: check that spawn interval decreases every 5 points
            # print(f"score: {game.score}\nspawn interval: {game.spawn_interval}")
            # # DEBUG end: check that spawn interval decreases every 5 points


# DEBUG start: use Button class to create text button called Test Button
## changes from white to pink when hovered over
test_button = Button(
    pos=(WIDTH // 2, 100),
    text_input="Test Button",
    font_path="fonts/love_days.ttf",
    fontsize=72,
    base_color="white",
    hovering_color="pink",
)


def draw():
    """draw() automatically by Pygame Zero when it needs to redraw your game window.
    It handles displaying the target, enemy movement, score,
    and game state (menu, playing, game over) on screen
    """
    screen.clear()  # erases old drawings when draw() is called

    for enemy in (
        game.enemies
    ):  # iterate for every item in game.enemies list, temp store in enemy var
        enemy.draw()  # draw Enemy obj stored in actor attribute

    target.draw()  # draw Target obj

    # Display current score
    screen.draw.text(
        f"Score: {game.score}",
        (10, 0),
        fontname="love_days",
        fontsize=100,
        owidth=1,
        ocolor="pink",
    )

    # DEBUG end: use Button class to create text button called Test Button
    ## changes from white to pink when hovered over
    test_button.draw(screen=screen)  # calls the Button draw method to draw onto screen


# start pygame zero game loop using Python interpreter to run
pgzrun.go()
