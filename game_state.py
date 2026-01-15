import sys
import pygame
from ui import Button

# TODO 1: Create a reset function in GameState class to clear old game data
## When RETRY button is clicked, game data needs to be reset.
### enemies, score, spawn timer, spawn interval,
### spawn decrease interval, difficulty score interval

# TODO 2: Create a draw method to display PLAY screen
## display background and current score


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
            self.game_over (bool): Boolean flag set to False to signal game is not over
        """

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
                pos=(960, 550),
                text_input="Start",
                font_path="fonts/love_days.ttf",
                fontsize=75,
                base_color="white",
                hovering_color="pink",
            ),
            "QUIT": Button(
                pos=(960, 700),
                text_input="Quit",
                font_path="fonts/love_days.ttf",
                fontsize=75,
                base_color="white",
                hovering_color="pink",
            ),
        }

        self.game_over_buttons = {
            "RETRY": Button(
                pos=(960, 550),
                text_input="Retry",
                font_path="fonts/love_days.ttf",
                fontsize=75,
                base_color="white",
                hovering_color="pink",
            ),
            "QUIT": Button(
                pos=(960, 700),
                text_input="Quit",
                font_path="fonts/love_days.ttf",
                fontsize=75,
                base_color="white",
                hovering_color="pink",
            ),
        }

        # Gameplay data
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 5

    def draw_menu(self, screen: object):
        """Draws the menu ui onto the screen.
        Background, buttons, ui elements.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # screen background
        screen.fill("black")

        # draws game title
        screen.draw.text(
            "CLICK DEFENSE",
            center=(960, 200),
            fontname="love_days",
            fontsize=100,
            color="purple",
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

        # screen background
        screen.fill("black")

        # Display current score
        screen.draw.text(
            f"Score: {self.score}",
            (10, 0),
            fontname="love_days",
            fontsize=72,
            owidth=1,
            ocolor="pink",
        )

    def draw_game_over(self, screen: object):
        """Draws the a GAMEOVER ui onto the screen.
        Background, buttons, ui elements.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # screen background
        screen.fill("black")

        # draw game over title
        screen.draw.text(
            "GAME OVER",
            center=(960, 200),
            fontname="love_days",
            fontsize=100,
            color="purple",
        )

        # draw final score
        screen.draw.text(
            f"Score: {self.score}",
            center=(960, 400),
            fontname="love_days",
            fontsize=80,
            color="blue",
        )

        # draw all the game_over_buttons
        for (
            btn
        ) in self.game_over_buttons.values():  # loops through key values: Button objs
            btn.draw(screen)  # calls Button draw() method

    def restart(self):
        """Cleans up game data and prepares for a fresh start"""

        # clear game data, reset back to default
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 5

        # change game state to PLAY
        self.state = "PLAY"

    def quit(self):
        """Quits and exits the game."""
        pygame.quit()  # Uninitalizes all pygame modules
        sys.exit()  # terminates Python process and closes game window
