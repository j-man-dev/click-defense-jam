import pygame  # Pygame Zero uses pygame under the hood


class Button:
    """This class is used to create buttons for UI."""

    def __init__(
        self,
        pos: tuple[int, int],
        text_input: str,
        font_path: str,
        fontsize: int,
        base_color: str | tuple[int, int, int],
        image_path: str | None = None,
        hovering_color: str | tuple[int, int, int] | None = None,
    ):
        """Initializes Button instance with set attribute values to create buttons.

        Args:
            pos (tuple[int, int]): (x, y) tuple, center position
            text_input (str): string for button name displayed
            font_path (str): path of font.ttf MUST include file extension. Ex: "fonts/myfont.ttf"
            fontsize (int): size of font
            base_color (str | tuple[int, int, int]): text color (R,G,B) or str (e.g. (255, 255, 255) or "white")
            image_path (str): path of image.png MUST include file extension. Ex: "images/myimage.png"
            hovering_color (str | tuple[int, int, int]): text hover color (R,G,B) or str (e.g. (255, 255, 255) or "white")
        """
        # create any rects, surfaces, starting values here
        self.x = pos[0]
        self.y = pos[1]
        self.text_input = text_input
        self.font_path = font_path
        self.fontsize = fontsize
        self.base_color = base_color
        self.image_path = image_path
        self.hover_color = hovering_color

        # Create Font object
        self.font = pygame.font.Font(self.font_path, self.fontsize)

        # Pre-render a Surface object (image) from a text
        self.text = self.font.render(self.text_input, True, self.base_color)

        # Pre-render a Surface object (image) for hovering_color text
        if self.hover_color is not None:
            self.hover = self.font.render(self.text_input, True, self.hover_color)

        # Pre-load a Surface object (image) from an image
        if self.image_path is not None:
            self.image = pygame.image.load(self.image_path)
        else:  # If image_path None, use the text Surface obj for our main Rect obj
            self.image = self.text

        # Create Rect obj from the image and text image aligned at pos center point
        self.image_rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def draw(self, screen: object):
        """Draws the image and text onto the screen at the specified position.

        Args:
            screen (obj): Pygame Zero Screen object that represents game screen
        """

        ## Get current mouse position at any given time
        MOUSE_POS = pygame.mouse.get_pos()

        ## select which pre-rendered Surface to use
        if self.image_rect.collidepoint(MOUSE_POS) and self.hover_color is not None:
            text_to_draw = self.hover
        else:
            text_to_draw = self.text  # re-renders to base_color when mouse not hovering

        # draw button
        if self.image_path is not None:
            screen.blit(self.image, self.image_rect)
        screen.blit(text_to_draw, self.text_rect)
