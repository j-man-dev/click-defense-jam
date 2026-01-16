import random
import sys
import pygame
from entities import ENEMY_ASSETS
from ui import Button

# TODO 2: Create global CONSTANT variables so its known not to change them

# Global constants
MAX_DIFFICULTY_SCORE = 240  # ((current_speed - start speed)//value_increased_by)*points required per interval
MAX_SPEED_CAP = 200
MIN_SPEED_CAP = 95
STAGE_COUNT = 10


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
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 5
        self.speed_min = 80  # px/sec
        self.speed_max = 80
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
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 10
        self.speed_min = 80  # px/sec
        self.speed_max = 80

        # change game state to PLAY + resets state_timer
        self.change_state("PLAY")

    def quit(self):
        """Quits and exits the game."""
        pygame.quit()  # Uninitalizes all pygame modules
        sys.exit()  # terminates Python process and closes game window

    # TODO 3: Create a method that gets the difficulty stage level based on game progression
    ## use LERP (linear interpolation) for smooth, natural progression
    ## it finds a value at a specific percentage b/w 2 points
    ## formula: start + (end - start) * progress -> never overshoots your cap
    ### start: Where you begin(Score 0, speed 80)
    ### end: Where you want to finish (Max speed = 200)
    ### progress: A value between 0.0 (0%) and 1.0 (100%).
    ### If you were at progress 0.5 (50%), you will be be halfway to a score of 240
    ### calculate current score progression towards the MAX_DIFFICULTY_SCORE.
    ### The max progress should only be 1.0 (100%) -> 240/240

    def get_difficulty_stage_progression(self):
        """Returns a float representing game progress (0.0 - 1.0) based on score and max difficuly score.

        Returns:
            float: progression value between 0.0 and 1.0 based on current score progress
        """
        # progress is a value b/w 0.0 (0%) and 1.0 (100%) so cap at 1.0
        return min(self.score / MAX_DIFFICULTY_SCORE, 1.0)  # selects lowest b/w the two

    # TODO 4: Create a function that retrieves enemy image based on stage and color index
    ## self.enemy_colors contain:
    ## ['black', 'blue', 'green', 'orange', 'pink', 'purple', 'red', 'teal', 'yellow']
    ## each color represents a stage, except last stage is random. index range 0-8 -> 9 colors
    ## current_stage = current progression % (0.0-1.0) of the STAGE_COUNT -> ex. 0.5 of 10 stages is stage 5
    ## color index for stage = current progression of STAGE_COUNT-1 bc indexing starts at 0
    ## use the index to call and store the color name
    ## use the color name to return the enemy image from ENEMY_ASSETS dictionary.
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
        """Difficulty-scaling: Increase spawn freq and speed based on points"""

        # Only run if requirements are met (e.g. every 5 points)
        if self.score > 0 and (
            self.score % self.difficulty_score_interval == 0
        ):  # cleanly divisble?
            # --- SCALE SPAWN FREQUENCY --- #
            # decreases interval by a percentage, capped at 0.2s
            self.spawn_interval = max(
                0.2, self.spawn_interval * (1 - self.spawn_interval_decrease)
            )

            # --- SCALE SPEED RANGE -- #
            # increase max speed by 5 every 10 points
            # Formula: 80 + (score // point trigger)*5
            # increase min speed after > 50 points by 2 every 10 points
            # Formula: 80 + ((score - 50))//10*5

            # max increases faster than min
            self.speed_max = 80 + (self.score // self.difficulty_score_interval) * 5

            # Min only starts increasing after 50 points.
            # -50 delay ensures that speed increase only by 2 at score 60 and not 12.
            if self.score > 50:
                self.speed_min = (
                    80 + ((self.score - 50) // self.difficulty_score_interval) * 1
                )

            # ensure that min and max have a cap speed range (100, 300)
            self.speed_min = min(self.speed_min, 95)
            self.speed_max = min(self.speed_max, 200)

    def get_spawn_speed(self) -> int:
        """Retrieves a random speed based on min/max speed

        Returns:
            int: returns a random speed within speed_min and speed_max range
        """
        return random.randint(self.speed_min, self.speed_max)
