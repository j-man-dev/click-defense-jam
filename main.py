import pgzrun
from typing import TYPE_CHECKING, Any

import pygame


from game_state import GameState
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


# Screen resolution 1280x720
WIDTH = 1920  # constant variable for horizontal size
HEIGHT = 1080  # constant variable for vertical size

# Instances of classes
game = GameState()
target = Target(
    image="cake1",
    image_path="images/cake1.png",
    screen_width=WIDTH,
    screen_height=HEIGHT,
)
player = Player(image_path="images/angry_cat.png")


def update(dt):
    """update() loop called automatically by Pygame Zero 60x/sec.
    It handles game logic: spawn rate, movement, collisions, spawn speed.

    Args:
        dt (float): delta time is time since last frame. Given automatically by Pygame Zero
    """

    # increment the state timer every frame. only resets during screen transition
    game.state_timer += dt

    # Enemy spawn when game state is "PLAY"
    if game.state == "PLAY":
        # Enemy spawn rate
        game.spawn_timer += dt  # spawn timer increases every frame by dt value

        if game.spawn_timer > game.spawn_interval:
            new_speed = game.get_spawn_speed()

            enemy = Enemy(
                image=game.get_enemy_image()["image"],
                image_path=game.get_enemy_image()["path"],
                speed=new_speed,
                screen_width=WIDTH,
                screen_height=HEIGHT,
            )
            game.enemies.append(
                enemy
            )  # New Enemy obj created and appended to enemies list
            game.spawn_timer = 0  # reset spawn timer after new enemy spawns
        for enemy in game.enemies:  # iterate through game.enemies Enemy obj list
            enemy.update(target, dt)  # update enemy angle to face target center

            # TODO 6: call the save data method when GAMEOVER AND data not yet saved
            ## NOTE: update() loops continues 60 fps even after GAMEOVER
            ## prevents data saved to JSON every 60fps after GAMEOVER True

            # --- PIXEL-PERFECT COLLISIOIN DETECTION ---#
            dx = int(enemy.mask_rect.left - target.mask_rect.left)  # left offset pos
            dy = int(enemy.mask_rect.top - target.mask_rect.top)  # top offset pos
            collision_point = target.mask.overlap(enemy.mask, (dx, dy))
            if collision_point:  # opaque pixels touch?
                game.change_state("GAMEOVER")  # state = GAMEOVER + reset state_timer
                pygame.mouse.set_visible(True)  # show regular mouse arrow
                # ONLY saves game if GAMEOVER and game not saved yet
                if game.state == "GAMEOVER" and not game.game_saved:  # default False
                    game.save_game()  # changes game_saved to true after saved

                    # Debug start: check if game was saved
                    # print(f"save status: {game.game_saved}")
                    # Debug end: check if game was saved
                return  # exits out of update() loop


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

    # only allows mouse clicks if screen has been visible for at least 0.5s
    if game.state_timer < 0.5:
        return

    if button == mouse.LEFT:
        # MENU screen actions
        if game.state == "MENU":
            # Start game when start clicked
            if game.menu_buttons["START"].image_rect.collidepoint(pos):
                game.change_state("PLAY")  # state = PLAY + reset state_timer
            # Quit and exit game when quit clicked
            elif game.menu_buttons["QUIT"].image_rect.collidepoint(pos):
                game.quit()
        # GAMEOVER screen actions
        elif game.state == "GAMEOVER":
            if game.game_over_buttons["RETRY"].image_rect.collidepoint(pos):
                game.reset()
            elif game.game_over_buttons["QUIT"].image_rect.collidepoint(pos):
                game.quit()

    # removes enemies when clicked and scales diffculty base on score
    for enemy in game.enemies:
        if button == mouse.LEFT and player.rect.colliderect(enemy.mask_rect):
            sounds.squish.play()  # plays squish sound when enemy clicked
            game.enemies.remove(enemy)
            game.score += 1
            # TODO 5: call the update highscore method every time a point is scored
            ### --- only call when score increases --- ###
            game.update_difficulty()  # checks if difficulty needs to be updated
            game.update_highscore()  # checks if highscore needs to be updated locally

            # # DEBUG start: check difficulty scaling speed and spawn freq
            # print(
            #     f"Score: {game.score} spawn interval: {game.spawn_interval} speed: {enemy.speed}"
            # )
            # # DEBUG end: check difficulty scaling speed and spawn freq


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
        target.draw()  # draw Target obj
        for enemy in (
            game.enemies
        ):  # iterate for every item in game.enemies list, temp store in enemy var
            enemy.draw()  # draw Enemy obj stored in actor attribute
        player.draw(screen=screen)


# start pygame zero game loop using Python interpreter to run
pgzrun.go()
