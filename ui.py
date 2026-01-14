import pygame  # Pygame Zero uses pygame under the hood


# TODO 1: Create Button class with parameters to create button UI element
## image, pos, text_input, fontname, fontsize, base_color,
## owidth(outline width), ocolor (ouline color), hovering_color

# TODO 2: if no image is given, create image from text
## pygame.font.Fonts(fontname, fontsize) -> returns Font obj
## use Font_obj.render(text, antialias, color) -> returns Pygame Surface

# TODO 3: create Rect obj from the image and the text image
## use Surface_obj.get_rect() method -> each loaded image is a Pygame surface

# TODO 4: Draw image and text on screen in def draw()
## use screen.blit(image, (left, top)) -> top-left is pos reference point
### so use image/text rect to center image on the pos provided as input arg

# TODO 5: Create event handling func for mouse hover
## Does mouse position hover over button, if so change color
## rect.collidepoint(pos) -> requires rect obj.


class Button:
    """This class is used to create buttons for UI."""

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

        # Create Rect obj from the image and text image aligned at pos center point
        self.image_rect = self.image.get_rect(center=(self.x, self.y))
        self.text_rect = self.text.get_rect(center=(self.x, self.y))

    def draw(self, screen: object):
        """Draws the image and text onto the screen at the specified position.

        Args:
            screen (obj): Pygame screen object that represents game screen
        """
        if self.image is not None:
            screen.blit(self.image, self.image_rect)
        screen.blit(self.text, self.text_rect)

    def change_color(self, pos: tuple[int, int]):
        """Changes button text color when mouse hovers over button.

        Args:
            pos (tuple[int, int]): (x, y) tuple, mouse position
        """
        if self.image_rect.collidepoint(pos):  # does mousepointer hover button rect?
            self.text = self.font.render(
                text=self.text_input, antialias=True, color=self.hover_color
            )  # change self.text color to hovering_color

    def update(self, dt=None):
        # move it, animate it, handle logic
        pass
