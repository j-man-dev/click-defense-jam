import json
from pathlib import Path
import random
import sys
import pygame
from entities import ENEMY_ASSETS
from ui import Button

# NOTE: game_state module focus on WHEN/WHERE/WHAT/HOW MANY to draw, consequences and performance
# Global constants
MAX_DIFFICULTY_SCORE = 240  # ((current_speed - start speed)//value_increased_by)*points required per interval
START_SPEED = 80  # always start speed at this value
MAX_SPEED_CAP = 200  # never let higher speed range go over this
MIN_SPEED_CAP = 95  # never let lower speed range go over this
STAGE_COUNT = 10  # number of difficulty stages in the game
MAX_SPAWN_CAP = 0.5  # never go below this spawn interval
MIN_SPAWN_CAP = 2  # never go over this spawn interval
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080


class GameState:
    def __init__(self):
        """Holds all the game state screen data and variables together (menu, play, end).

        Attributes:
            self.state(str): game state as "MENU", "PLAY", "GAMEOVER", "PAUSE", "RESUME"
            self.render_map (dict): maps self.state to reference draw screen methods (draw_menu, draw_play, draw_game_over)
            self.menu_buttons(dict): creates menu buttons using Button class and stores them
            self.game_over_buttons (dict): creates game buttons using Button class and stores them
            self.enemies (list): Store list of Enemy Actor objects. 0 enemies at start
            self.score (int): tracks player's score. Start at 0
            self.storage.setdefault (dict):
            self.spawn_timer (int): timer counting in secs since last spawn. Starts at 0.
            self.spawn_interval (int): Define how often enemy spawn per sec
            self.spawn_interval_decrease (int): amount of secs to decrease spawn_interval by
            self.difficulty_score_interval (int): points required to trigger difficulty
            self.speed_min (int): defines min speed (px/sec) of the enemy
            self.speed_max (int): defines max speed (px/sec) of the enemy
            self.save_path(object): Path object that represents file location
            self.data(dict): centralized data from JSON game_data file
            self.game_saved(bool): bool flag indicating whether or not game was saved
            self.new_highscore(bool): bool flag indicating whether or not new highscore achieved
        """

        self.save_path = Path("game_data.json")  # Path obj of file path
        # --- CENTRALIZED DATA DICTIONARY --- #
        ## add to the dictionary as game grows (e.g. player_name, sound_vol. etc.)
        self.data = {"highscore": 0}

        # Gameplay data
        self.game_saved = False  # set to False game has not been saved yet
        self.is_resuming = True  # game is not paused by default
        self.resume_countdown = 0  # tracks countdown sec til going back to play state
        self.enemies = []
        self.enemy_colors = list(ENEMY_ASSETS.keys())  # retrieves the enemy color names
        self.score = 0
        self.highscore = 0
        self.new_highscore = False  # new highscore was achieved?
        self.spawn_timer = 0
        self.spawn_interval = MIN_SPAWN_CAP
        self.speed_min = START_SPEED  # px/sec
        self.speed_max = START_SPEED
        self.state_timer = 0

        # Current screen/mode (menu, playing, game_over)
        self.state = "MENU"  # "MENU", "PLAY", "GAMEOVER", "PAUSE"

        # Map self.state to reference draw screen methods
        self.render_map = {
            "MENU": self.draw_menu,
            "PLAY": self.draw_play,
            "GAMEOVER": self.draw_game_over,
            "PAUSE": self.draw_pause,
        }

        # Composition: Create buttons for menu and game over screesn in GameState __init__
        self.menu_buttons = {
            "START": Button(
                pos=(960, 580),
                text_input="Start",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),  # pink
            ),
            "QUIT": Button(
                pos=(960, 750),
                text_input="Quit",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),  # pink
            ),
        }

        self.game_over_buttons = {
            "RETRY": Button(
                pos=(960, 580),
                text_input="Retry",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),  # pink
            ),
            "QUIT": Button(
                pos=(960, 750),
                text_input="Quit",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),  # pink
            ),
        }
        # loads existing data immediately
        self.load_save()

    ## --- # NOTE: GAME PERSISTENCE LOGIC --- ##
    def load_save(self):
        """Reads the saved json data file if it exits, otherwise it keeps the default"""
        if self.save_path.exists():  # save_path exists?
            # opens file, then reads with utf-8 encoder, store value as variable game_data_file
            with open(self.save_path, "r", encoding="utf-8") as game_data_file:
                # turns json to python dict then updates local data dict with saved values
                self.data.update(json.load(game_data_file))

        # sets self.highscore with whatever value is stored in local central data dict.
        self.highscore = self.data["highscore"]

        # DEBUG start: check data successfully loaded
        # print(f"Data successfully loaded: {self.data}")
        # DEBUG end: check data successfully loaded

    def save_game(self):
        """Call this ONLY when game over or player exits.
        Optimize speed by reducing times accessing JSON"""

        # opens file, then writes with utf-8 encoder, store value as variable game_data_file
        with open(self.save_path, "w", encoding="utf-8") as game_data_file:
            # saves the data to the opened file and indents 4 spaces for human readability
            json.dump(self.data, game_data_file, indent=4)

        self.game_saved = True  # True when game is saved

    def update_highscore(self):
        """Update the highscore value in memory only (locally), for easy access in code
        and to optimize speed by reducing read/write to JSON file.

        Args:
            current_score (int): current score during gameplay
        """
        if self.score > self.highscore:
            self.highscore = self.score  # for easy access in code
            self.data["highscore"] = self.score  # to later save to JSON data file
            self.new_highscore = True  # new highscore is achieved

    ## --- # NOTE: RENDER COORDINATION DRAW LOGIC (WHEN/WHERE/WHAT/HOW MANY) --- ##
    # TODO 3: Create a method that toggles mouse pointer visiblity based on game state
    ## MENU: mouse arrow visible
    ## PAUSE, PLAY, GAMEOVER: mouse arrow invisible
    ## hide default mouse arrow bc it will be replaced with player sprite

    def update_mouse_visibility(self):
        """Hides mouse arrow on all screens except MENU because all other screens
        will display the Player sprite over the mouse arrow.

        """
        if self.state == "MENU":
            pygame.mouse.set_visible(True)
        else:  # state is any other screen
            pygame.mouse.set_visible(False)

    def draw_menu(self, screen: object):
        """Draws the menu ui onto the screen.
        Background, buttons, ui elements.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # set window caption
        pygame.display.set_caption("Cake Defender - Menu")

        # screen background
        screen.blit("menu", (0, 0))

        # draw outline text button
        screen.draw.text(
            "Start",
            center=(960, 580),
            fontname="love_days",
            fontsize=99,
            owidth=1,
            ocolor=(154, 207, 174),  # green
        )
        screen.draw.text(
            "Quit",
            center=(960, 750),
            fontname="love_days",
            fontsize=99,
            owidth=1,
            ocolor=(154, 207, 174),  # green
        )

        if self.highscore > 0:
            screen.draw.text(
                f"Highscore: {self.highscore}",
                center=(960, 930),
                fontname="love_days",
                fontsize=110,
                color=(191, 138, 105),
            )

        # draw all the menu_buttons
        for btn in self.menu_buttons.values():  # loop through key values: Button obj
            btn.draw(screen)  # calls Button draw() method

    def draw_play(self, screen: object):
        """Draws the a gameplay ui onto the screen.
        Background and current score.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # set window caption
        pygame.display.set_caption("Cake Defender")

        # screen background
        screen.blit("play_screen", (0, 0))

        # Display current score
        screen.draw.text(
            f"Score: {self.score}",
            (100, 0),
            fontname="love_days",
            fontsize=72,
            owidth=1,
            ocolor=(154, 207, 174),  # green
        )

    def draw_pause(self, screen: object):
        """Draws the a PAUSE ui onto the screen.
        PAUSE text and instruction on how to resume.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # set window caption
        pygame.display.set_caption("Cake Defender - Pause")

        # -- screen background -- #

        # Create overlay Surface = screen size. Use pygame.Surface with SRCALPHA to enable transparency
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # use Surface_obj.fill() to fill overlay Surface with semi-transparent black color
        ## (0, 0, 0, 128) -> R,G,B,A -> A (alpha) 0-255, 0 is full transparency
        overlay.fill((0, 0, 0, 128))

        # draw the semi-transparent overlay screen on top the PLAY screen
        # use screen.blit(Surface, pos) with enabled alpha. Requires pygame.Surface as arg
        screen.blit(overlay, (0, 0))  # top-left pos 0, 0

        # draw UI TEXT on top of overlay
        screen.draw.text(
            "PAUSED",
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            fontname="love_days",
            fontsize=80,
        )

        # Draw PAUSE screen if is_resuming is False.
        if not self.is_resuming:
            screen.draw.text(
                "Press space to resume",
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
                fontname="love_days",
                fontsize=60,
            )

        # draw resuming text countdown from 3 to 1, rounding as decr by -= dt
        if self.is_resuming:
            screen.draw.text(
                f"Resuming in {round(self.resume_countdown)}",
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100),
                fontname="love_days",
                fontsize=60,
                color="orange",
            )

    def draw_game_over(self, screen: object):
        """Draws the a GAMEOVER ui onto the screen.
        Background, buttons, ui elements.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # set window caption
        pygame.display.set_caption("Cake Defender - Game Over")

        # screen background
        screen.blit("game_over", (0, 0))

        # draw final score
        if self.new_highscore:  # new highscore?
            score_text = f"New Highscore: {self.score}"
        else:
            score_text = f"Score: {self.score}"
        screen.draw.text(
            score_text,
            center=(960, 465),
            fontname="love_days",
            fontsize=110,
            color="orange",
        )

        # Add extra screen assets
        screen.blit("heart", (780, 570))  # heart near RETRY button
        screen.blit("ghost1", (795, 740))  ## ghost near QUIT button

        # draw outline text button
        screen.draw.text(
            "Retry",
            center=(960, 580),
            fontname="love_days",
            fontsize=99,
            owidth=1,
            ocolor=(154, 207, 174),
        )
        screen.draw.text(
            "Quit",
            center=(960, 750),
            fontname="love_days",
            fontsize=99,
            owidth=1,
            ocolor=(154, 207, 174),
        )

        # draw all the game_over_buttons
        for (
            btn
        ) in self.game_over_buttons.values():  # loops through key values: Button objs
            btn.draw(screen)  # calls Button draw() method

    ## --- # NOTE: GAME STATE MANAGEMENT LOGIC --- ##

    def change_state(self, new_state: str):
        """Central hub for all screen transitions

        Args:
            new_state (str): Must be a game state "MAIN", "PLAY", "GAMEOVER"
        """
        self.state = new_state
        self.state_timer = 0  # resets timer buffer for new screen

    # TODO 8: refactor: move game resuming logic to GameState
    ## it tells WHEN to check resume countdown, CONSEQUENCES of countdown
    def resume(self, dt):
        self.resume_countdown -= dt  # decreases resume_countdown
        if self.resume_countdown <= 0:
            self.is_resuming = False  # game no longer resuming
            self.change_state("PLAY")

    def reset(self):
        """Cleans up game data and prepares for a fresh start"""

        # clear game data, reset back to default
        self.game_saved = False
        self.is_resuming = True  # game is not paused by default
        self.resume_countdown = 0
        self.enemies = []
        self.score = 0
        self.new_highscore = False
        self.spawn_timer = 0
        self.spawn_interval = MIN_SPAWN_CAP
        self.speed_min = START_SPEED
        self.speed_max = START_SPEED
        self.state_timer = 0

        # change game state to PLAY + resets state_timer
        self.change_state("PLAY")

    def quit(self):
        """Quits and exits the game."""
        pygame.quit()  # Uninitalizes all pygame modules
        sys.exit()  # terminates Python process and closes game window

    ## --- # NOTE: GAME LOGIC --- ##

    def get_difficulty_stage_progression(self):
        """Return a float representing stage progress (0.0 - 1.0) based on score milestones
        Where MAX_DIFFICULTY_SCORE determines number of stages.

        Returns:
            float: progression value between 0.0 and 1.0 based on current score progress
        """
        # progress is the current score out of max difficulty score
        # which gives a value b/w 0.0 (0%) and 1.0 (100%) so cap at 1.0
        return min(self.score / MAX_DIFFICULTY_SCORE, 1.0)  # selects lowest b/w the two

    def get_enemy_image(self):
        """Determines enemy image name based on score and stage difficulty"""
        progression = self.get_difficulty_stage_progression()

        # stores the index number 0-8
        stage_color_index = int(progression * (STAGE_COUNT - 1))

        # LOGICS
        # if index is 0-8: return the specific color from the self.enemy_colors list
        # if index is 9 or greater: return a random color from the list

        if stage_color_index >= 9:
            color_key = random.choice(self.enemy_colors)
        else:
            color_key = self.enemy_colors[stage_color_index]

        return ENEMY_ASSETS[color_key]  # returns dict of enemy image based on color

    def update_difficulty(self):
        """Difficulty-scaling: Increase spawn freq and speed based score progression.
        Uses LERP Linear interoperability formula for smooth progression.
        Progression based on each point earned. start + (end - start) * progression
        """

        # updates difficulty infinitesimally after every point earned
        progress = self.get_difficulty_stage_progression()  # progression based on score

        # --- SCALE SPAWN FREQUENCY --- #
        # cap max spawn interval to ensure it doesn't go below 0.5 using max()
        self.spawn_interval = max(
            0.5, MIN_SPAWN_CAP + (MAX_SPAWN_CAP - MIN_SPAWN_CAP) * progress
        )

        # --- SCALE SPEED RANGE -- #
        ## LERP linear interoperability (progress) b/w start (80) and speed cap
        # cap min and max speed to ensure it doesn't go over the defined cap (95 and 200)
        self.speed_min = min(
            START_SPEED + (MIN_SPEED_CAP - START_SPEED) * progress, MIN_SPEED_CAP
        )
        self.speed_max = min(
            START_SPEED + (MAX_SPEED_CAP - START_SPEED) * progress, MAX_SPEED_CAP
        )

    def get_spawn_speed(self) -> float:
        """Retrieves a random float based on min/max speed to increase smooth movement variety

        Returns:
            float: returns a random speed within speed_min and speed_max range
        """
        return random.uniform(self.speed_min, self.speed_max)

    ## --- # NOTE: GAME FLOW LOGIC --- ##
    # TODO 6: refactor: move spawn logic function to GameState class
    ## GameState handles WHEN/WHERE/WHAT/HOW MANY to draw

    def update_spawn(self, dt: float, enemy_class: object):
        """Handles enemy spawning logic based on difficulty progression.
        New enemy spawn color changes based on stage level

        Args:
            enemy_class(object): object created from Enemy class which defines what the enemy is
            dt (float): delta time is time since last frame. Given automatically by Pygame Zero

        Returns:
            list: returns list of enemy objects stored inside game.enemies list
        """

        self.spawn_timer += dt  # spawn timer increases every frame by dt value

        if self.spawn_timer > self.spawn_interval:
            new_speed = self.get_spawn_speed()

            # Enemy object created
            enemy = enemy_class(
                image=self.get_enemy_image()["image"],
                image_path=self.get_enemy_image()["path"],
                speed=new_speed,
                screen_width=SCREEN_WIDTH,
                screen_height=SCREEN_HEIGHT,
            )
            # New Enemy obj created and appended to enemies list
            self.enemies.append(enemy)
            self.spawn_timer = 0  # reset spawn timer after new enemy spawns

    # TODO 7: refactor: Move collision and enemy update logic to GameState class
    ## Gamestate handles WHAT/CONSEQUENCES (what collides, consquences of collision)

    def update_enemies(self, target: object, dt: float):
        """Moves enemy toward target, removes enemies when they are killed and adds to the score

        Args:
            target (object): A Target class instance used to define what the objective is
            dt (float): delta time is time since last frame. Given automatically by Pygame Zero
        """
        self.target = target
        for enemy in self.enemies[:]:  # [:] freezes dynamic list to modify safely
            enemy.update(self.target, dt)  # "Move toward target!"
            # debug: commented out to debug while placeholder not available. uncomment to exit debug
            # if (
            #     enemy.is_dead
            # ):  # NOTE: PLACEHOLDER until enemy_player collision logic refactored
            #     self.enemies.remove(enemy)
            #     self.score += 1

    def update_enemy_target_collision(self, target: object, dt: float):
        """Returns True if game over triggered by a collision + saves game.

        Args:
            target (object): A Target class instance used to define what the objective is
            dt (float): delta time is time since last frame. Given automatically by Pygame Zero

        Returns:
            bool: True if there is a collison and False if there isn't
        """
        self.target = target
        for enemy in self.enemies:  # iterate through game.enemies Enemy obj list
            # --- PIXEL-PERFECT COLLISIOIN DETECTION ---#
            dx = int(
                enemy.mask_rect.left - self.target.mask_rect.left
            )  # left offset pos
            dy = int(enemy.mask_rect.top - self.target.mask_rect.top)  # top offset pos
            # checks if target and enemy mask collide/overlap -> returns True if it does
            game_over = self.target.mask.overlap(enemy.mask, (dx, dy))

            if game_over:  # enemy and target collide?
                self.change_state("GAMEOVER")  # state = GAMEOVER + reset state_timer
                # ONLY saves game if GAMEOVER and game not saved yet
                if not self.game_saved:  # default False
                    self.save_game()  # changes game_saved to true after saved
                return True  # game is over
        return False  # False all enemies in loop -> no collision
