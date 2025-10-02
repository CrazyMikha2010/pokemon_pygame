
import random
from static.config import SCREEN_SIZE
from pokemon import WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon


class World:
    """
    Represents the game world containing Pokemons.
    """
    def __init__(self, n_pok: int, facade) -> None:
        self.facade = facade
        self.n_pok = n_pok
        self.pokemons: list = []
        self._pokemons_types = [WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon]
        self._generate_pokemons()

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

    def catch_pokemon(self, pos: tuple) -> object | None:
        """Attempts to catch a Pokemon at the given position."""
        for pokemon in self.pokemons:
            rect = pokemon.im.get_rect()
            if rect.left + pokemon.x <= pos[0] <= rect.right + pokemon.x and rect.top + pokemon.y <= pos[1] <= rect.bottom + pokemon.y:
                self.pokemons.remove(pokemon)
                return pokemon
        return None