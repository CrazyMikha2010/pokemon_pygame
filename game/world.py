import random
from static.config import SCREEN_SIZE, TRAINER_SIZE
from static.colors import WHITE
from pokemon import WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon
from trainer import SmartTrainer
from typing import List


class World:
    """
    Represents the game world containing Pokemons.
    """
    def __init__(self, n_pok: int, facade: 'PygameFacade') -> None:
        """
        Initializes the World instance.

        Args:
            n_pok (int): Number of Pokemons to generate.
            facade (PygameFacade): The pygame facade.
        Returns:
            None
        """
        self.facade = facade
        self.n_pok = n_pok
        self.pokemons: List['Pokemon'] = []
        self._pokemons_types = [WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon]
        self._generate_pokemons()
        self.trainer1: SmartTrainer = SmartTrainer("Данияр", facade, facade.load_image("game/static/images/trainer 1.png", TRAINER_SIZE), facade.load_image("game/static/images/trainer 11.png", TRAINER_SIZE), 10, 20)
        self.trainer2: SmartTrainer = SmartTrainer("Тяночка", facade, facade.load_image("game/static/images/trainer 2.png", TRAINER_SIZE), facade.load_image("game/static/images/trainer 2.png", TRAINER_SIZE), 600, 20, True)

    def _generate_pokemons(self) -> None:
        """
        Initializes Pokemons in the world.
        """
        for i in range(self.n_pok):
            pokemon_cls = random.choice(self._pokemons_types)
            name = f'test{i + 1}'
            x = random.randint(200, SCREEN_SIZE[0] - 200)
            y = random.randint(0, SCREEN_SIZE[1])
            self.pokemons.append(pokemon_cls(name, self.facade, x, y))

    def add(self, event: tuple) -> None:
        """
        Adds a new Pokemon at the given event position.

        Args:
            event (tuple): Position (x, y) to add the Pokemon.
        Returns:
            None
        """
        pokemon_cls = random.choice(self._pokemons_types)
        name = f'test{len(self.pokemons) + 1}'
        x, y = event
        self.pokemons.append(pokemon_cls(name, self.facade, x, y))

    def draw(self) -> None:
        """
        Draws all Pokemons and Trainers in the world.
        """
        self.facade.draw_text(250, 10, f'Выбирает: {self.trainer1.name if self.trainer1.ischoosing else self.trainer2.name}', WHITE, 50)
        for pokemon in self.pokemons:
            pokemon.draw()
        self.trainer1.draw()
        self.trainer2.draw()

    def update(self) -> None:
        """
        Updates all Pokemons' positions.

        Args:
            None
        Returns:
            None
        """
        for pokemon in self.pokemons:
            pokemon.move()

    def catch_pokemon(self, pos: tuple) -> None:
        """
        Attempts to catch a Pokemon at the given position.

        Args:
            pos (tuple): Position (x, y) to catch the Pokemon.
        Returns:
            bool: True if a Pokemon was caught, False otherwise.
        """
        flag: bool = False
        for pokemon in self.pokemons:
            rect = pokemon.im.get_rect()
            if rect.left + pokemon.x <= pos[0] <= rect.right + pokemon.x and rect.top + pokemon.y <= pos[1] <= rect.bottom + pokemon.y:
                self.pokemons.remove(pokemon)
                if self.trainer1.ischoosing:
                    self.trainer1.add(pokemon)
                else:
                    self.trainer2.add(pokemon)
                flag = True
                break
        self.trainer1.ischoosing, self.trainer2.ischoosing = self.trainer2.ischoosing, self.trainer1.ischoosing
        return flag