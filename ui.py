import pygame  # Pygame Zero uses pygame under the hood


# TODO 1: Create Button class with parameters to create button UI element
## image, pos, text_input, fontname, fontsize, base_color,
## owidth(outline width), ocolor (ouline color), hovering_color

# TODO 2: if no image is given, create image from text
## pygame.font.Fonts(fontname, fontsize) -> returns Font obj
## use Font_obj.render(text, antialias, color) -> returns Pygame Surface

# TODO 3: create Rect obj from the image and the text image
## use Surface_obj.get_rect() method -> each loaded image is a Pygame surface


class Button:
    """This class is used to create buttons for UI element."""

    def __init__(
        self,
        pos: tuple[int, int],
        text_input: str,
        fontname: str,
        fontsize: int,
        base_color: tuple[int, int, int],
        image: str | None = None,
        owidth: int | None = None,
        ocolor: str | None = None,
        hovering_color: tuple[int, int, int] | None = None,
    ):
        """Initializes Button instance with set attribute values to create buttons.

        Args:
            pos (tuple[int, int]): (x, y) tuple, center position
            text_input (str): string for button name displayed
            fontname (str): file name of font style in fonts directory
            fontsize (int): size of font
            base_color (tuple[int, int, int]): (R,G,B) for normal text
            image (str): pygame.Surface or None
            owidth (int): optional thickness value for text outline. int or None
            ocolor (str): optional text outline color. str or None
            hovering_color (tuple[int, int, int]): optional (R,G,B) text color when mouse hover. tuple or None
        """
        # create any rects, surfaces, starting values here
        self.image = image
        self.x = pos[0]
        self.y = pos[1]
        self.text_input = text_input
        self.fontname = fontname
        self.fontsize = fontsize
        self.base_color = base_color
        self.owidth = owidth
        self.ocolor = ocolor
        self.hover_color = hovering_color

        # Create Font object
        self.font = pygame.font.Font(self.fontname, self.fontsize)

        # Create an image from text
        self.text = self.font.render(
            text=self.text_input, antialias=True, color=self.base_color
        )

        # If no image is given, use the text surface as the main rect
        if self.image is None:
            self.image = self.text

        # Create Rect obj from the image and text image and align center points
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        # draw your thing on the screen
        pass

    def update(self, dt=None):
        # move it, animate it, handle logic
        pass

    def handle_event(self, event_data):
        # optional: clicks, keyboard, etc.
        pass
