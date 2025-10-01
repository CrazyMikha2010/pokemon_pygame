from static.config import *

class Trainer:
    def __init__(self, name: str, facade, im1, im2, x: int, y: int, ischoosing: bool=False) -> None:
        self.wins = 0
        self.box = []
        self.name = name
        self.facade = facade
        self.im1 = im1
        self.im2 = im2
        self.x = x
        self.y = y
        self.ischoosing = ischoosing

    def add(self, pokemon: 'Pokemon') -> None:
        self.box.append(pokemon)

    def best_team(self, n: int) -> list:
        team = []
        for i in range(n):
            team.append(self.box.pop()) 
        return team
    
    def draw(self, has_won: bool=False) -> None:
        if has_won:
            self.x = SCREEN_SIZE[0] // 2 - self.im1.get_width() // 2
            self.y = 50
            self.facade.draw_text(self.x-10, self.y - 30, f'Победитель: {self.name}', WHITE, 30)
            self.facade.draw_text(self.x-10, self.y - 10, f'Побед: {self.wins}', WHITE, 30)
            self.facade.draw_image(self.x, self.y, self.im1)
            return
        if len(self.box) == 0:
            s = "Нет покемонов в команде"
        elif len(self.box) == 1:
            s = "1 покемон в команде"
        elif 2 <= len(self.box) <= 4:
            s = f"{len(self.box)} покемона в команде"
        else:
            s = f"{len(self.box)} покемонов в команде"
        self.facade.draw_text(self.x-10, self.y, s, WHITE)
        if not self.ischoosing:
            self.facade.draw_image(self.x, self.y, self.im1)
        else:
            self.facade.draw_image(self.x, self.y, self.im2)

class SmartTrainer(Trainer):
    def best_team(self, n :int) -> list:
        self.box.sort(key=lambda x: x.atk * 2 + x.df)
        team = []
        if len(self.box) < n:
            n = len(self.box)
        for _ in range(n):
            team.append(self.box.pop()) 
        return team