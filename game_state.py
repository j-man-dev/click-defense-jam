import random
import sys
import pygame
from ui import Button

# TODO 1: Add min and max speed attributes for randomized speed variation


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
        self.speed_min = 80  # px/sec
        self.speed_max = 80

    def draw_menu(self, screen: object):
        """Draws the menu ui onto the screen.
        Background, buttons, ui elements.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # set window caption
        pygame.display.set_caption("Cake Defender - Menu")

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

        # set window caption
        pygame.display.set_caption("Cake Defender")

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

        # set window caption
        pygame.display.set_caption("Cake Defender - Game Over")

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

    # TODO 3: update restart() method to reset speed_min and speed_max values

    def restart(self):
        """Cleans up game data and prepares for a fresh start"""

        # clear game data, reset back to default
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 5
        self.speed_min = 80  # px/sec
        self.speed_max = 80

        # change game state to PLAY
        self.state = "PLAY"

    def quit(self):
        """Quits and exits the game."""
        pygame.quit()  # Uninitalizes all pygame modules
        sys.exit()  # terminates Python process and closes game window

    # TODO 2: create a method updates the difficulty speed and spawn freqency

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
            # increase max speed by 10 every 5 points
            # Formula: 80 + (score // point trigger)*10
            # increase min speed after > 50 points by 5 every double max speed points
            # Formula: 80 + ((score - 50))//10*5

            # max increases faster than min
            self.speed_max = 80 + (self.score // self.difficulty_score_interval) * 10

            # Min only starts increasing after 50 points.
            # -50 delay ensures that speed doesn't increase only by 5 at score 60 and not 30.
            if self.score > 50:
                self.speed_min = (
                    80 + ((self.score - 50) // (self.difficulty_score_interval * 2)) * 5
                )

            # ensure that min and max have a cap speed range (100, 300)
            self.speed_min = min(self.speed_min, 95)
            self.speed_max = min(self.speed_max, 200)

    # TODO 4: create a method that retrieves the new spawn speed variation range
    ## return the min and max speed

    def get_spawn_speed(self) -> int:
        """Retrieves a random speed based on min/max speed

        Returns:
            int: returns a random speed within speed_min and speed_max range
        """
        return random.randint(self.speed_min, self.speed_max)
