import pygame
from static.config import POKEMON_SIZE
NOT_STARTED = -1
STARTED = 0
HIT_DELAY = 0


class Battle:
    """
    Handles the battle logic between two trainers and their teams.
    """
    def __init__(self, n: int, x: int, y: int, facade: 'PygameFacade') -> None:
        self.n = n
        self.x = x
        self.y = y
        self.facade = facade
        self.turn = 1
        self.state = NOT_STARTED
        self.is_end: bool = False
        self.hit_circle = pygame.Surface(POKEMON_SIZE, pygame.SRCALPHA)
        self.button_rect = None

    def draw(self, surface) -> None:
        """
        Draws the battle scene and highlights the current turn.

        Args:
            surface: The pygame surface to draw on.
        Returns:
            None
        """
        if self.state == NOT_STARTED:
            return
        for pokemon in self.team1 + self.team2:
            pokemon.draw()
        if self.team1 and self.team2:
            self.facade.draw_line(self.team1[0].x + self.team1[0].rect.midright[0], self.team1[0].y + self.team1[0].rect.midright[1], self.team2[0].x + self.team2[0].rect.midleft[0], self.team2[0].y + self.team2[0].rect.midleft[1], (255, 0, 0), 3)
            self.facade.draw_line(self.team2[0].x + self.team2[0].rect.midleft[0], self.team2[0].y + self.team2[0].rect.midleft[1], self.team1[0].x + self.team1[0].rect.midright[0], self.team1[0].y + self.team1[0].rect.midright[1], (255, 0, 0), 3)

            pygame.draw.circle(self.hit_circle, (255, 0, 0, 100), self.hit_circle.get_rect().center, self.hit_circle.get_rect().width//2 - 5, 0)

            if self.turn == 1:
                surface.blit(self.hit_circle, (self.team2[0].rect.topleft[0] + self.team2[0].x, self.team2[0].rect.topleft[1] + self.team2[0].y))
            else:
                surface.blit(self.hit_circle, (self.team1[0].rect.topleft[0] + self.team1[0].x, self.team1[0].rect.topleft[1] + self.team1[0].y))


    def start(self, trainer1: 'SmartTrainer', trainer2: 'SmartTrainer') -> None:
        """
        Starts a new battle between two trainers.

        Args:
            trainer1: The first trainer.
            trainer2: The second trainer.
        Returns:
            None
        """
        if self.state == NOT_STARTED:
            self.trainer1 = trainer1
            self.trainer2 = trainer2
            self.team1 = trainer1.best_team(self.n)
            self.copy1 = self.team1[:]
            self.team2 = trainer2.best_team(self.n)
            self.copy2 = self.team2[:]
            if len(self.team1) == 0 or len(self.team2) == 0:
                self.end()
                return

            y = self.y
            for pokemon in self.team1:
                pokemon.x, pokemon.y = self.x, y
                y += 70 + 10
                pokemon.vx = pokemon.vy  = 0
            y = self.y
            for pokemon in self.team2:
                pokemon.x, pokemon.y = self.x + 280, y
                y += 70 + 10
                pokemon.vx = pokemon.vy = 0
            self.state = STARTED
            self.last_update = pygame.time.get_ticks()


    def update(self) -> None:
        """
        Updates the battle state.

        Args:
            None
        Returns:
            None
        """
        if self.state == STARTED:
            self.facade.draw_line(self.team1[0].x, self.team1[0].y + 5, self.team1[0].x + 50 * (self.team1[0].hp/100), self.team1[0].y + 5, (255 * (100 - self.team1[0].hp) / 100, 255 * self.team1[0].hp / 100, 0), 5)
            self.facade.draw_line(self.team2[0].x, self.team2[0].y + 5, self.team2[0].x + 50 * (self.team2[0].hp/100), self.team2[0].y + 5, (255  * (100 - self.team2[0].hp) / 100, 255 * self.team2[0].hp / 100, 0), 5)
            self.trainer1.draw()
            self.trainer2.draw()
            nowTime = pygame.time.get_ticks() 
            if nowTime - self.last_update > HIT_DELAY:
                self.last_update = nowTime
            else:
                return
            if self.turn == 1 and len(self.team1) > 0 and len(self.team2) > 0:
                self.team1[0].attack(self.team2[0])
                if self.team2[0].hp <= 0:
                    self.team2.remove(self.team2[0])
                if len(self.team2) == 0:
                    return self.finish(1)
            elif self.turn == 2 and len(self.team1) > 0 and len(self.team2) > 0:
                self.team2[0].attack(self.team1[0])
                if self.team1[0].hp <= 0:
                    self.team1.remove(self.team1[0])
                if len(self.team1) == 0:
                    return self.finish(2)
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1

    def finish(self, result: int) -> None:
        """
        Handles the end of a battle round.

        Args:
            result: The result of the battle (1 or 2).
        Returns:
            None
        """
        self.state = NOT_STARTED
        if result == 1:
            self.trainer1.wins += 1
            for p in self.copy1:
                p.hp = 100
                self.trainer1.add(p)
        else:
            self.trainer2.wins += 1
            for p in self.copy2:
                p.hp = 100
                self.trainer2.add(p)
        self.start(self.trainer1, self.trainer2)

    def end(self) -> None:
        """
        Ends the battle and logs the winner to a file.

        Args:
            None
        Returns:
            None
        """
        self.facade.clear_screen()
        winner = self.trainer1 if self.trainer1.wins > self.trainer2.wins else self.trainer2
        winner.draw(True)
        self.button_rect = self.facade.draw_button(200, 300, 150, 50, 'Заново', (0, 128, 0), (255, 255, 255), 60)
        self.save_log(winner)

    def save_log(self, winner: 'Trainer') -> None:
        """
        Saves the battle winner to a log file.

        Args:
            winner: The winning Trainer object.
        Returns:
            None
        """
        import os
        log_dir = 'game/logs'
        os.makedirs(log_dir, exist_ok=True)
        with open(os.path.join(log_dir, 'battle_winner.txt'), 'a', encoding='utf-8') as log_file:
            log_file.write(f'Winner: {winner.name}\n')

    def started(self) -> bool:
        """
        Returns True if the battle has started.

        Args:
            None
        Returns:
            bool: True if the battle has started, False otherwise.
        """
        return self.state == STARTED