import random
from static.config import SCREEN_SIZE, TRAINER_SIZE
from pokemon import WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon
from trainer import SmartTrainer


class World:
    """
    Represents the game world containing Pokemons.
    """
    def __init__(self, n_pok: int, facade: 'PygameFacade') -> None:
        self.facade = facade
        self.n_pok = n_pok
        self.pokemons: list = []
        self._pokemons_types = [WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon]
        self._generate_pokemons()
        self.trainer1 = SmartTrainer("Данияр", facade, facade.load_image("game/static/images/trainer 1.png", TRAINER_SIZE), facade.load_image("game/static/images/trainer 11.png", TRAINER_SIZE), 10, 20)
        self.trainer2 = SmartTrainer("Тяночка", facade, facade.load_image("game/static/images/trainer 2.png", TRAINER_SIZE), facade.load_image("game/static/images/trainer 2.png", TRAINER_SIZE), 600, 20, True)

    def _generate_pokemons(self) -> None:
        """Initializes Pokemons in the world."""
        for i in range(self.n_pok):
            pokemon_cls = random.choice(self._pokemons_types)
            name = f'test{i + 1}'
            x = random.randint(200, SCREEN_SIZE[0] - 200)
            y = random.randint(0, SCREEN_SIZE[1])
            self.pokemons.append(pokemon_cls(name, self.facade, x, y))

    def add(self, event: tuple) -> None:
        """Adds a new Pokemon at the given event position."""
        pokemon_cls = random.choice(self._pokemons_types)
        name = f'test{len(self.pokemons) + 1}'
        x, y = event
        self.pokemons.append(pokemon_cls(name, self.facade, x, y))

    def draw(self) -> None:
        """Draws all Pokemons in the world."""
        for pokemon in self.pokemons:
            pokemon.draw()

    def update(self) -> None:
        """Updates all Pokemons' positions."""
        for pokemon in self.pokemons:
            pokemon.move()

    def catch_pokemon(self, pos: tuple) -> None:
        """Attempts to catch a Pokemon at the given position."""
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