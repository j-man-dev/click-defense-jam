import random
import sys
import pygame
from entities import ENEMY_ASSETS
from ui import Button


# Global constants
MAX_DIFFICULTY_SCORE = 240  # ((current_speed - start speed)//value_increased_by)*points required per interval
START_SPEED = 80  # always start speed at this value
MAX_SPEED_CAP = 200  # never let higher speed range go over this
MIN_SPEED_CAP = 95  # never let lower speed range go over this
STAGE_COUNT = 10  # number of difficulty stages in the game
MAX_SPAWN_CAP = 0.5  # never go below this spawn interval
MIN_SPAWN_CAP = 2  # never go over this spawn interval


class GameState:
    def __init__(self):
        """Holds all the game state screen data and variables together (menu, play, end).

        Attributes:
            self.state(str): game state as "menu", "playing" and "game_over"
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
        """

        # Current screen/mode (menu, playing, game_over)
        self.state = "MENU"  # "MENU", "PLAY", "GAMEOVER"

        # Gameplay data
        self.enemies = []
        self.enemy_colors = list(ENEMY_ASSETS.keys())  # retrieves the enemy color names
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = MIN_SPAWN_CAP
        self.speed_min = START_SPEED  # px/sec
        self.speed_max = START_SPEED
        self.state_timer = 0

        # Map self.state to reference draw screen methods
        self.render_map = {
            "MENU": self.draw_menu,
            "PLAY": self.draw_play,
            "GAMEOVER": self.draw_game_over,
        }

        # Composition: Create buttons for menu and game over screesn in GameState __init__
        self.menu_buttons = {
            "START": Button(
                pos=(960, 580),
                text_input="Start",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),
            ),
            "QUIT": Button(
                pos=(960, 750),
                text_input="Quit",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),
            ),
        }

        self.game_over_buttons = {
            "RETRY": Button(
                pos=(960, 580),
                text_input="Retry",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),
            ),
            "QUIT": Button(
                pos=(960, 750),
                text_input="Quit",
                font_path="fonts/love_days.ttf",
                fontsize=100,
                base_color="white",
                hovering_color=(236, 140, 128),
            ),
        }

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

        # draw all the menu_buttons
        for btn in self.menu_buttons.values():  # loop through key values: Button obj
            btn.draw(screen)  # calls Button draw() method

    def draw_play(self, screen: object):
        """Draws the a gameplay ui onto the screen.
        Background and current score.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """
        # hide default mouse arrow bc it will be replaced with player sprite
        pygame.mouse.set_visible(False)

        # set window caption
        pygame.display.set_caption("Cake Defender")

        # screen background
        screen.blit("play_screen", (0, 0))

        # Display current score
        screen.draw.text(
            f"Score:{self.score}",
            (100, 0),
            fontname="love_days",
            fontsize=72,
            owidth=1,
            ocolor=(154, 207, 174),
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
        screen.draw.text(
            f"Score:{self.score}",
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

    def change_state(self, new_state: str):
        """Central hub for all screen transitions

        Args:
            new_state (str): Must be a game state "MAIN", "PLAY", "GAMEOVER"
        """
        self.state = new_state
        self.state_timer = 0  # resets timer buffer for new screen

    def restart(self):
        """Cleans up game data and prepares for a fresh start"""

        # clear game data, reset back to default
        self.enemies = []
        self.score = 0
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
