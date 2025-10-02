from static.config import SCREEN_SIZE, WHITE
from typing import List

class Trainer:
    """
    Represents a Pokemon trainer.
    """
    def __init__(self, name: str, facade, im1, im2, x: int, y: int, ischoosing: bool = False) -> None:
        self.wins: int = 0
        self.box: List['Pokemon'] = []
        self.name = name
        self.facade = facade
        self.im1 = im1
        self.im2 = im2
        self.x = x
        self.y = y
        self.ischoosing = ischoosing

    def add(self, pokemon: 'Pokemon') -> None:
        """Adds a Pokemon to the trainer's box."""
        self.box.append(pokemon)

    def best_team(self, n: int) -> List['Pokemon']:
        """Selects the best team of n Pokemons from the box."""
        team = []
        for _ in range(min(n, len(self.box))):
            team.append(self.box.pop())
        return team
    
    def draw(self, has_won: bool = False) -> None:
        """Draws the trainer and their status."""
        if has_won:
            self.x = SCREEN_SIZE[0] // 2 - self.im1.get_width() // 2
            self.y = 50
            self.facade.draw_text(self.x - 10, self.y - 30, f'Победитель: {self.name}', WHITE, 30)
            self.facade.draw_text(self.x - 10, self.y - 10, f'Побед: {self.wins}', WHITE, 30)
            self.facade.draw_image(self.x, self.y, self.im1)
            return
        s = self._team_status()
        self.facade.draw_text(self.x - 10, self.y, s, WHITE)
        self.facade.draw_image(self.x, self.y, self.im2 if self.ischoosing else self.im1)

    def _team_status(self) -> str:
        """Returns a string describing the team status."""
        n = len(self.box)
        if n == 0:
            return "Нет покемонов в команде"
        elif n == 1:
            return "1 покемон в команде"
        elif 2 <= n <= 4:
            return f"{n} покемона в команде"
        else:
            return f"{n} покемонов в команде"

class SmartTrainer(Trainer):
    """
    A smarter trainer that picks the best team based on attack and defense.
    """
    def best_team(self, n: int) -> List['Pokemon']:
        self.box.sort(key=lambda x: x.atk * 2 + x.df)
        team = []
        for _ in range(min(n, len(self.box))):
            team.append(self.box.pop())
        return team