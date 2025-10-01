import pygame

class PygameFacade:
    def __init__(self, screen_size: tuple, caption: str='Noname') -> None:
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()

    def draw_circle(self, x: int, y: int, color, radius: int) -> None:
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_rectangle(self, x: int, y: int, width: int, height: int, color) -> None:
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color, width: int) -> None:
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

    def load_image(self, path: str, size: tuple):
        im = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(im, size)

    def draw_image(self, x: int, y: int, im) -> None:
        self.screen.blit(im, (x, y))

    def update_screen(self) -> None:
        pygame.display.flip()

    def clear_screen(self) -> None:
        self.screen.fill((0, 0, 0))

    def draw_text(self, x: int, y: int, text: str, color, font_size=24) -> None:
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))