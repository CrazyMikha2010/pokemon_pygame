import pygame
from world import World
from battle import Battle
from static.config import FPS, pygame_facade

class EventHandler:
    def __init__(self) -> None:
        """
        Initializes the EventHandler and resets the game state.
        """
        self._reset()

    def _reset(self) -> None:
        """
        Resets the world, battle, and game flags.
        """
        self.world = World(10, pygame_facade)
        self.battle = Battle(5, 250, 60, pygame_facade)
        self.running = True
        self.flag = False
        self.show_restart = False

    def handle_input(self) -> None:
        """
        Handles user input events (mouse, quit, restart).
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_restart and self.battle.button_rect and self.battle.button_rect.collidepoint(event.pos):
                    self._reset()
                elif not self.show_restart:
                    if not self.world.catch_pokemon(event.pos):
                        self.world.add(event.pos)

    def _is_catching(self) -> bool:
        """
        Checks if trainers are still catching Pokemons.

        Args:
            None
        Returns:
            bool: True if catching, False otherwise.
        """
        return not len(self.world.trainer1.box) >= 5 or not len(self.world.trainer2.box) >= 5
    
    def update(self) -> None:
        """
        Updates the game state, drawing and progressing world/battle.
        """
        if not self.show_restart: pygame_facade.clear_screen()
        if self._is_catching() and not self.flag:
            self.world.draw()
            self.world.update()
        else:
            self.flag = True
            if not self.battle.started() and not self.show_restart:
                self.battle.start(self.world.trainer1, self.world.trainer2)
            elif not self.show_restart:
                self.battle.update()
                if len(self.battle.team1) == 0 or len(self.battle.team2) == 0:
                    self.battle.end()
                    self.show_restart = True
                    
            if not self.show_restart: 
                self.battle.draw(pygame_facade.screen)
            
        pygame_facade.update_screen()
        pygame_facade.clock.tick(FPS)