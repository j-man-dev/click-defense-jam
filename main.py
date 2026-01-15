import pgzrun
from typing import TYPE_CHECKING, Any

from game_state import GameState
from entities import Enemy, Target

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

    # Enemy spawn when game state is "PLAY"
    if game.state == "PLAY":
        # Enemy spawn rate
        game.spawn_timer += dt  # spawn timer increases every frame by dt value

        if game.spawn_timer > game.spawn_interval:
            enemy = Enemy(image="enemy", screen_width=WIDTH, screen_height=HEIGHT)
            game.enemies.append(
                enemy
            )  # New Enemy obj created and appended to enemies list
            game.spawn_timer = 0  # reset spawn timer after new enemy spawns
        for enemy in game.enemies:  # iterate through game.enemies Enemy obj list
            enemy.update(target, dt)  # update enemy angle to face target center

            # PIXEL-PERFECT COLLISIOIN DETECTION
            dx = int(enemy.mask_rect.left - target.mask_rect.left)  # left offset pos
            dy = int(enemy.mask_rect.top - target.mask_rect.top)  # top offset pos
            collision_point = target.mask.overlap(enemy.mask, (dx, dy))
            if collision_point:  # opaque pixels touch?
                game.state = "GAMEOVER"  # set state to GAMEOVER
                return  # exits out of update() loop


# TODO 1: On game over screen, if RETRY button is clicked, restart the game
## game data is reset to default settings:


def on_mouse_down(pos, button):
    """Called automatically by Pygame zero
    Mouse clicks handlings the following event hooks:
    Left click on enemies remove them.
    Main menu button clicks starts or exits game.
    Game over screen button clicks restarts or exits game.

    Args:
        pos (tuple): (x, y) tuple that gives location of mouse pointer when button pressed.
        button (obj): A mouse enum value indicating the button that was pressed.
    """
    if button == mouse.LEFT:
        # MENU screen actions
        if game.state == "MENU":
            # Start game when start clicked
            if game.menu_buttons["START"].image_rect.collidepoint(pos):
                game.state = "PLAY"
            # Quit and exit game when quit clicked
            elif game.menu_buttons["QUIT"].image_rect.collidepoint(pos):
                game.quit()
        # GAMEOVER screen actions
        elif game.state == "GAMEOVER":
            if game.game_over_buttons["RETRY"].image_rect.collidepoint(pos):
                game.restart()
            elif game.game_over_buttons["QUIT"].image_rect.collidepoint(pos):
                game.quit()

    # removes enemies when clicked
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


def draw():
    """draw() automatically by Pygame Zero when it needs to redraw your game window.
    It handles displaying the target, enemy movement, score,
    and game state (menu, playing, game over) on screen
    """
    screen.clear()  # erases old drawings when draw() is called

    # Use current game.state value to decide what to draw. Default value set to "MENU"
    game.render_map[game.state](screen=screen)  # calls draw methods based on state

    # display when playing
    if game.state == "PLAY":
        for enemy in (
            game.enemies
        ):  # iterate for every item in game.enemies list, temp store in enemy var
            enemy.draw()  # draw Enemy obj stored in actor attribute

        target.draw()  # draw Target obj


# start pygame zero game loop using Python interpreter to run
pgzrun.go()
