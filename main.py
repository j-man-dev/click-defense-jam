import pgzrun
from typing import TYPE_CHECKING, Any

from game_state import GameState, SCREEN_HEIGHT, SCREEN_WIDTH
from entities import Enemy, Player, Target


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
    storage: Any

    # Below are classes/methods.
    class Actor:
        pass


# Screen resolution
WIDTH = SCREEN_WIDTH  # constant variable for horizontal size
HEIGHT = SCREEN_HEIGHT  # constant variable for vertical size

# Instances of classes
game = GameState()
target = Target(
    image="cake1",
    image_path="images/cake1.png",
    screen_width=WIDTH,
    screen_height=HEIGHT,
)
player = Player(image_path="images/cat_angry.png")


# TODO 9: refactor: clean up using GameState methods
## use spawn enemies, update enemies, and collision logic methods


def update(dt):
    """update() loop called automatically by Pygame Zero 60x/sec.
    It handles game logic: spawn rate, movement, collisions, spawn speed.

    Args:
        dt (float): delta time is time since last frame. Given automatically by Pygame Zero
    """

    if game.state == "PAUSE" and game.is_resuming:  # game resuming?
        game.resume(dt)

    # increment the state timer every frame. only resets during screen transition
    game.state_timer += dt
    # Enemy spawn when game state is "PLAY"
    if game.state == "PLAY":
        game.update_spawn(dt=dt, enemy_class=Enemy)  # spawns enemy
        game.update_enemies(target=target, dt=dt)  # moves enemies
        if game.update_enemy_target_collision(target, dt):  # is game over?
            return  # exits out of update() loop


def on_key_down(key):  # key stores key press input
    """reads if key pressed is space to pause and resume game.
    When space pressed on PAUSE state, it resumes the game and sets countdown.
    When space pressed on PLAY state, it pauses the game.

    Args:
        key (enum): reads key press inputs
    """

    if key == key.SPACE:  # is space pressed?
        if game.state == "PLAY":
            game.change_state("PAUSE")  # DISPLAY PAUSE SCREEN and pause game
        elif game.state == "PAUSE":
            game.is_resuming = True
            game.resume_countdown = 3.0


# TODO 11: refactor: update event hook method using GameState method
## replace collision logic


def on_mouse_down(pos, button):
    """Called automatically by Pygame zero
    Mouse clicks handlings the following event hooks:
    Left click enemies remove them.
    Start - Play screen.
    Retry - Play screen
    Quit - closes window

    Args:
        pos (tuple): (x, y) tuple that gives location of mouse pointer when button pressed.
        button (obj): A mouse enum value indicating the button that was pressed.
    """

    # block input during PAUSE state
    if game.state == "PAUSE":
        return  # exits out of function

    # only allows mouse clicks if screen has been visible for at least 0.5s
    if game.state_timer < 0.5:
        return

    # Finds which button was clicked on MENU/GAMEOVER screen then changes game state
    game.check_button_interactions(
        mouse_pos=pos, input_button=button, expected_button=mouse.LEFT
    )
    # DEBUG start: print what the state is after button is pressed
    print(f"mouse click change state {game.state}. state timer: {game.state_timer}")
    # DEBUG start: print what the state is after button is pressed

    # removes enemies when clicked and scales diffculty base on score
    game.check_enemy_player_collisions(
        input_button=button,
        expected_button=mouse.LEFT,
        player=player,
    )


# TODO 12: refactor: Move WHAT/WHERE to draw code to GameState class
## it tells WHAT entities to draw and WHERE which screens/state to draw them
# TODO 13: refactor: Update draw() using GameState methods


def draw():
    """draw() automatically by Pygame Zero when it needs to redraw your game window.
    It handles displaying the target, enemy movement, score,
    and game state (menu, playing, game over) on screen
    """
    screen.clear()  # erases old drawings when draw() is called

    # TODO 4: call the update_mouse_visiblity() method in draw

    # sets mouse visibility to True/False base on game state
    game.update_mouse_visibility()

    if game.state == "PAUSE":
        game.draw_play(screen)
        target.draw()  # draw Target obj
        # iterate for every item in game.enemies list, temp store in enemy var
        for enemy in game.enemies:
            enemy.draw()  # draw Enemy obj stored in actor attribute

    # Use current game.state value to decide what to draw. Default value set to "MENU"
    # debug: comment code below to enter debug. uncomment to exit debug
    game.render_map[game.state](screen=screen)  # calls draw methods based on state

    # TODO 5: add visibility of Player sprite in both PLAY and GAMEOVER state

    # display when playing
    if game.state == "PLAY":
        target.draw()  # draw Target obj
        # iterate for every item in game.enemies list, temp store in enemy var
        for enemy in game.enemies:
            enemy.draw()  # draw Enemy obj stored in actor attribute
    if game.state == "PLAY" or game.state == "GAMEOVER":
        player.draw(screen=screen)


# start pygame zero game loop using Python interpreter to run
pgzrun.go()
