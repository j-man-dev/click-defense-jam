from ui import Button

# TODO goal: create methods in GameState class that draws each screen state when called

# TODO 1: Add attributes for menu data and current screen state
## state: menu, playing, game_over
## render map: map game state to screen methods
## menu selection: start, quit selection
## create buttons required for each state screen

# TODO 2: create the draw menu screen method
## requires screen as input parameter
## fill the screen with a background
## draw text for game title
## draw all the menu_buttons on the menu screen


class GameState:
    def __init__(self):
        """Holds all the game state screen data and variables together (menu, play, end).

        Attributes:
            self.state(str): game state as "menu", "playing" and "game_over"
            self.render_map (dict): maps self.state to reference draw screen methods (draw_menu, draw_play, draw_game_over)
            self.menu_selection (str): user's button selection on menu. 0=start, 1=quit
            self.menu_buttons(dict): creates menu buttons using Button class and stores them
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

        # Menu data
        self.menu_selection = 0

        # Composition: Create menu buttons inside GameState
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

        # Gameplay data
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 5

        # Game over data
        self.game_over = False

    def draw_menu(self, screen: object):
        """Draws the the menu onto the screen.
        Background, buttons, ui elements.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        # screen background
        screen.fill("black")

        # draws game title
        screen.draw.text(
            "CAKE DEFENDER",
            center=(960, 200),
            fontname="love_days",
            fontsize=100,
        )

        # draw all the menu_buttons
        for btn in self.menu_buttons.values():  # loop through key value: Button obj
            btn.draw(screen)  # calls Button draw() method

    # placeholder for play screen
    def draw_play(self, screen: object):
        pass

    # placehodler for game over screen
    def draw_game_over(self, screen: object):
        pass
