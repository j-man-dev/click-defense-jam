from ui import Button

# TODO goal: create methods in GameState class that draws each screen state when called

# TODO 1: Add attributes for menu data and current screen state
## state: menu, playing, game_over
## render map: map game state to screen methods
## menu selection: start, quit selection
## create buttons required for each state screen


class GameState:
    def __init__(self):
        """Holds all the game state screen data and variables together (menu, play, end).

        Attributes:
            self.state(str): game state as "menu", "playing" and "game_over"
            self.menu_selection (str): user's button selection on menu. 0=start, 1=quit
            self.enemies (list): Store list of Enemy Actor objects. 0 enemies at start
            self.score (int): tracks player's score. Start at 0
            self.spawn_timer (int): timer counting in secs since last spawn. Starts at 0.
            self.spawn_interval (int): Define how often enemy spawn per sec
            self.spawn_interval_decrease (int): amount of secs to decrease spawn_interval by
            self.difficulty_score_interval (int): points required to trigger difficulty
            self.game_over (bool): Boolean flag set to False to signal game is not over
        """

        # Current screen/mode (menu, playing, game_over)
        self.state = "MENU"

        # Map game state to reference draw screen methods
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
                pos=(850, 550),
                text_input="Start",
                font_path="fonts/love_days.ttf",
                fontsize=75,
                base_color="white",
                hovering_color="pink",
            ),
            "QUIT": Button(
                pos=(860, 700),
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
