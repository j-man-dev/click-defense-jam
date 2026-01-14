class GameState:
    def __init__(self):
        """Holds all the game state data variables together (menu, play, end).

        Attributes:
            self.enemies (list): Store list of Enemy Actor objects. 0 enemies at start
            self.score (int): tracks player's score. Start at 0
            self.spawn_timer (int): timer counting in secs since last spawn. Starts at 0.
            self.spawn_interval (int): Define how often enemy spawn per sec
            self.spawn_interval_decrease (int): amount of secs to decrease spawn_interval by
            self.difficulty_score_interval (int): points required to trigger difficulty
            self.game_over (bool): Boolean flag set to False to signal game is not over
        """
        # Current screen/mode (menu, playing, game_over)

        # Menu data

        # Gameplay data
        self.enemies = []
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 2
        self.spawn_interval_decrease = 0.1
        self.difficulty_score_interval = 5

        # Game over data
        self.game_over = False
