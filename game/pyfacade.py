import pygame

def singleton(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton
class PygameFacade:
    """
    Facade for common pygame operations (drawing, image loading, etc).
    """
    def __init__(self, screen_size: tuple, caption: str = 'Noname') -> None:
        """Initializes the pygame window and clock."""
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def draw_circle(self, x: int, y: int, color: tuple, radius: int) -> None:
        """Draws a circle on the screen."""
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: tuple) -> None:
        """Draws a rectangle on the screen."""
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color, width: int) -> None:
        """Draws a line on the screen."""
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

    @staticmethod
    def load_image(path: str, size: tuple) -> pygame.Surface:
        """Loads and scales an image from the given path."""
        im = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(im, size)

    def draw_image(self, x: int, y: int, im: pygame.Surface) -> None:
        """Draws an image at the given position."""
        self.screen.blit(im, (x, y))

    def update_screen(self) -> None:
        """Updates the display to show all drawn elements."""
        pygame.display.flip()

    def clear_screen(self) -> None:
        """Clears the screen to black."""
        self.screen.fill((0, 0, 0))

    def draw_text(self, x: int, y: int, text: str, color, font_size: int = 24) -> None:
        """Draws text on the screen at the given position."""
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))

    def draw_button(self, x: int, y: int, width: int, height: int, text: str, button_color, text_color, font_size: int) -> pygame.Rect:
        """Draws button and returns its hitbox."""
        self.draw_rectangle(x, y, width, height, button_color)
        self.draw_text(x + 2, y + 2, text, text_color, font_size)
        self.update_screen()
        return pygame.Rect(x, y, width, height)