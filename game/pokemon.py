from static.config import *

class Pokemon:
    def __init__(self, name: str, facade, im, x: int, y: int, atk: int = 5, df: int = 5) -> None:
        self.facade = facade
        self.hp = 100
        self.name = name
        self.atk = atk
        self.df = df
        self.blackout = False
        self.x = x
        self.y = y
        self.vx = random.randint(1, 10)
        self.vy = random.randint(1, 10)
        self.im = im
        self.mask = pygame.mask.from_surface(im)
        self.ischosen = False
        self.rect = self.im.get_rect()

    @property
    def hp(self) -> int:
        return self.__hp

    @hp.setter
    def hp(self, value: int) -> None:
        self.__hp = max(value, 0)

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def atk(self) -> int:
        return self.__atk

    @atk.setter
    def atk(self, value: int) -> None:
        self.__atk = max(value, 0)

    @property
    def df(self) -> int:
        return self.__df

    @df.setter
    def df(self, value: int) -> None:
        self.__df = max(value, 0)

    def attack(self, other: 'Pokemon', mult: int = 1, div: float = 1) -> None:
        if self.hp <= 0 or other.hp <= 0:
            return
        damage = max(self.atk * mult - int(other.df * div), 1)
        other.hp -= damage

    def draw(self) -> None:
        if not self.ischosen:
            self.facade.draw_image(self.x, self.y, self.im)
    
    def move(self) -> None:
        if self.ischosen: return
        self.x += self.vx
        self.y += self.vy
        if self.x < 200 or self.x > SCREEN_SIZE[0] - 200:
            self.vx *= -1
            self.x = 200 if self.x < 200 else SCREEN_SIZE[0] - 200
        if self.y < 0 or self.y > SCREEN_SIZE[1]:
            self.vy *= -1
            self.y = 0 if self.y < 0 else SCREEN_SIZE[1]

class WaterPokemon(Pokemon):
    def __init__(self, name: str, facade, x: int, y: int, atk: int = 5, df: int = 5) -> None:
        super().__init__(name, facade, facade.load_image(random.choice(water_paths), POKEMON_SIZE), x, y, atk, df)

    def attack(self, other: Pokemon, mult: int = 1, div: float = 1) -> None:
        mult = 1 + 2 * isinstance(other, FirePokemon)
        return super().attack(other, mult=mult)

class FirePokemon(Pokemon):
    def __init__(self, name: str, facade, x: int, y: int, atk: int = 5, df: int = 5) -> None:
        super().__init__(name, facade, facade.load_image(random.choice(fire_paths), POKEMON_SIZE), x, y, atk, df)

    pass

class GrassPokemon(Pokemon):
    def __init__(self, name: str, facade, x: int, y: int, atk: int = 5, df: int = 5) -> None:
        super().__init__(name, facade, facade.load_image(random.choice(grass_paths), POKEMON_SIZE), x, y, atk, df)

    def attack(self, other: Pokemon, mult: int = 1, div: float = 1) -> None:
        div = 1 + 1 * isinstance(other, FirePokemon)
        return super().attack(other, div=1/div)

class ElectricPokemon(Pokemon):
    def __init__(self, name: str, facade, x: int, y: int, atk: int = 5, df: int = 5) -> None:
        super().__init__(name, facade, facade.load_image(random.choice(electric_paths), POKEMON_SIZE), x, y, atk, df)

    def attack(self, other: Pokemon, mult: int = 1, div: float = 1) -> None:
        div = 1 * (not isinstance(other, WaterPokemon))
        return super().attack(other, div=div)
