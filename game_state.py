import json
from pathlib import Path
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
            self.save_path(object): Path object that represents file location
            self.data(dict): centralized data from JSON game_data file
            self.game_saved(bool): bool flag indicating whether or not game was saved
            self.new_highscore(bool): bool flag indicating whether or not new highscore achieved
        """

        # TODO 1: Define attributes: game data path, centralized data dictionary
        ## Use pathlib Path class to create Path obj for the game data JSON
        ## create local centralized data dictionary defining highscore as 0
        ## create highscore attr that gets highscore from centralized data dict.

        self.save_path = Path("game_data.json")  # Path obj of file path
        # --- CENTRALIZED DATA DICTIONARY --- #
        ## add to the dictionary as game grows (e.g. player_name, sound_vol. etc.)
        self.data = {"highscore": 0}

        # Gameplay data
        self.game_saved = False  # set to False game has not been saved yet
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
        self.state = "MENU"  # "MENU", "PLAY", "GAMEOVER"

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

    # TODO 2: Create load game data method that loads data JSON to centralized data dict.
    ## check that the file path location exists. use .exists() method
    ## open/read the JSON data (safe: encode using uft-8 to handle future special symbols)
    ### use with open(path obj, 'r' , encoding="utf-8"), 'r' as file: read mode
    ##  use .update(json.load(opened file)) to move the opened file data to central data dict
    ## update the highscore attr with the value updated in centralized data
    ## call this method immediately in __init__ to load save data to central data dict

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

    # TODO 3: Create method that updates local highscore
    ## if the current score > highscore, replace highscore with current score
    ## and update the centralized data dict with the current score

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

    # TODO 4: Create method that saves the game data to the JSON data file
    ## open/write the JSON data with the current centralized data dictionary
    ### use with open(path obj, 'w', encoding=)
    ### use json.dump(data, opened file, indent=4) add 4 space indents to file for human readability
    ## call only when game over or player exits to optimize speed (reduce accessing JSON)
    ## add boolean flag that indicates the game was saved. add as attr default = False

    def save_game(self):
        """Call this ONLY when game over or player exits.
        Optimize speed by reducing times accessing JSON"""

        # opens file, then writes with utf-8 encoder, store value as variable game_data_file
        with open(self.save_path, "w", encoding="utf-8") as game_data_file:
            # saves the data to the opened file and indents 4 spaces for human readability
            json.dump(self.data, game_data_file, indent=4)

        self.game_saved = True  # True when game is saved

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

        # TODO 8: if highscore > 0 then display it on menu screen below quit
        ## text color: (191, 138, 105) brown
        # Draw highest score data
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
        # hide default mouse arrow bc it will be replaced with player sprite
        pygame.mouse.set_visible(False)

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

        # TODO 7: display "New Highscore: <score>" if highscore achieved, otherwise display "Score: <score> ".
        ## create a boolean flag that indicates whether or not new highscore was achieved
        ### add it in __init__ and then it gets updated if update_highscore() cond. is met
        ## at game end, update_highscore() already set highscore = score if score > highscore
        ## position below QUIT button

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

    def change_state(self, new_state: str):
        """Central hub for all screen transitions

        Args:
            new_state (str): Must be a game state "MAIN", "PLAY", "GAMEOVER"
        """
        self.state = new_state
        self.state_timer = 0  # resets timer buffer for new screen

    def reset(self):
        """Cleans up game data and prepares for a fresh start"""

        # clear game data, reset back to default
        self.game_saved = False
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
