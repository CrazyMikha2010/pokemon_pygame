from static.config import *
from pokemon import *
from world import *

class World:
    def __init__(self, n_pok: int, facade) -> None:
        self.facade = facade
        self.n_poc = n_pok
        self.pokemons = []
        self.pokemons_list = [WaterPokemon, FirePokemon, GrassPokemon, ElectricPokemon]
        self.generate_pokemones()

    def generate_pokemones(self) -> None:
        for _ in range(self.n_poc):
            self.pokemons.append(random.choice(self.pokemons_list)(f'test{len(self.pokemons) + 1}', self.facade, random.randint(200, SCREEN_SIZE[0] - 200), random.randint(0, SCREEN_SIZE[1]), atk=random.randint(1, MAX_POKEMON_ATK), df=random.randint(1, MAX_POKEMON_DF)))

    def add(self, event:tuple) -> None:
        self.pokemons.append(random.choice(self.pokemons_list)(f'test{len(self.pokemons) + 1}', pygame_facade, event[0], event[1]))

    def draw(self) -> None:
        for pokemon in self.pokemons:
            pokemon.draw()

    def update(self) -> None:
        for pokemon in self.pokemons:
            pokemon.move()

    def catch_pokemon(self, pos: tuple):
        for pokemon in self.pokemons:
            rect = pokemon.im.get_rect()
            if rect.left + pokemon.x <= pos[0] <= rect.right + pokemon.x and rect.top + pokemon.y <= pos[1] <= rect.bottom + pokemon.y:
                self.pokemons.remove(pokemon)
                return pokemon
        return None