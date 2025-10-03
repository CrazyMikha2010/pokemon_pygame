from static.config import *


class Pokemon:
    """
    Base class for all Pokemon types.
    """
    def __init__(self, name: str, facade: 'PygameFacade', im, x: int, y: int) -> None:
        """
        Initializes a Pokemon instance.

        Args:
            name (str): The name of the Pokemon.
            facade (PygameFacade): The pygame facade.
            im: The image surface for the Pokemon.
            x (int): X position.
            y (int): Y position.
        Returns:
            None
        """
        self.facade = facade
        self.hp: int = 100
        self.name = name
        self.atk: int = random.randint(0, MAX_POKEMON_ATK)
        self.df: int = random.randint(0, MAX_POKEMON_DF)
        self.blackout: bool = False
        self.x = x
        self.y = y
        self.vx: int = random.randint(-10, 10)
        self.vy: int = random.randint(-10, 10)
        self.im = im
        self.mask = pygame.mask.from_surface(im)
        self.ischosen: bool = False
        self.rect = self.im.get_rect()


    @property
    def hp(self) -> int:
        """
        Returns the current HP.

        Args:
            None
        Returns:
            int: Current HP value.
        """
        return self.__hp

    @hp.setter
    def hp(self, value: int) -> None:
        self.__hp = max(value, 0)

    @property
    def name(self) -> str:
        """
        Returns the Pokemon's name.

        Args:
            None
        Returns:
            str: Pokemon name.
        """
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        self.__name = value

    @property
    def atk(self) -> int:
        """
        Returns the attack value.

        Args:
            None
        Returns:
            int: Attack value.
        """
        return self.__atk

    @atk.setter
    def atk(self, value: int) -> None:
        self.__atk = max(value, 0)

    @property
    def df(self) -> int:
        """
        Returns the defense value.

        Args:
            None
        Returns:
            int: Defense value.
        """
        return self.__df

    @df.setter
    def df(self, value: int) -> None:
        self.__df = max(value, 0)


    def attack(self, other: 'Pokemon', mult: int = 1, div: float = 1) -> None:
        """
        Attacks another Pokemon.

        Args:
            other (Pokemon): The target Pokemon.
            mult (int): Attack multiplier.
            div (float): Defense divisor.
        Returns:
            None
        """
        if self.hp <= 0 or other.hp <= 0:
            return
        damage = max(self.atk * mult - int(other.df * div), 1)
        other.hp -= damage

    def draw(self) -> None:
        """
        Draws the Pokemon on the screen.
        """
        if not self.ischosen:
            self.facade.draw_image(self.x, self.y, self.im)
    
    def move(self) -> None:
        """
        Moves the Pokemon within the screen bounds.
        """
        if self.ischosen:
            return
        self.x += self.vx
        self.y += self.vy
        if self.x < 200 or self.x > SCREEN_SIZE[0] - 200:
            self.vx *= -1
            self.x = 200 if self.x < 200 else SCREEN_SIZE[0] - 200
        if self.y < 0 or self.y > SCREEN_SIZE[1]:
            self.vy *= -1
            self.y = 0 if self.y < 0 else SCREEN_SIZE[1]


class WaterPokemon(Pokemon):
    """
    Water type Pokemon.
    """
    def __init__(self, name: str, facade, x: int, y: int) -> None:
        """
        Initializes a Water type Pokemon.

        Args:
            name (str): The name of the Pokemon.
            facade (PygameFacade): The pygame facade.
            x (int): X position.
            y (int): Y position.
        Returns:
            None
        """
        super().__init__(name, facade, facade.load_image(random.choice(water_paths), POKEMON_SIZE), x, y)

    def attack(self, other: 'Pokemon', mult: int = 1, div: float = 1) -> None:
        """
        Attacks another Pokemon, with bonus against Fire type.

        Args:
            other (Pokemon): The target Pokemon.
            mult (int): Attack multiplier.
            div (float): Defense divisor.
        Returns:
            None
        """
        mult = 1 + 2 * isinstance(other, FirePokemon)
        return super().attack(other, mult=mult)


class FirePokemon(Pokemon):
    """
    Fire type Pokemon.
    """
    def __init__(self, name: str, facade, x: int, y: int) -> None:
        """
        Initializes a Fire type Pokemon.

        Args:
            name (str): The name of the Pokemon.
            facade (PygameFacade): The pygame facade.
            x (int): X position.
            y (int): Y position.
        Returns:
            None
        """
        super().__init__(name, facade, facade.load_image(random.choice(fire_paths), POKEMON_SIZE), x, y)


class GrassPokemon(Pokemon):
    """
    Grass type Pokemon.
    """
    def __init__(self, name: str, facade, x: int, y: int) -> None:
        """
        Initializes a Grass type Pokemon.

        Args:
            name (str): The name of the Pokemon.
            facade (PygameFacade): The pygame facade.
            x (int): X position.
            y (int): Y position.
        Returns:
            None
        """
        super().__init__(name, facade, facade.load_image(random.choice(grass_paths), POKEMON_SIZE), x, y)

    def attack(self, other: 'Pokemon', mult: int = 1, div: float = 1) -> None:
        """
        Attacks another Pokemon, with penalty against Fire type.

        Args:
            other (Pokemon): The target Pokemon.
            mult (int): Attack multiplier.
            div (float): Defense divisor.
        Returns:
            None
        """
        div = 1 + 1 * isinstance(other, FirePokemon)
        return super().attack(other, div=1/div)


class ElectricPokemon(Pokemon):
    """
    Electric type Pokemon.
    """
    def __init__(self, name: str, facade, x: int, y: int) -> None:
        """
        Initializes an Electric type Pokemon.

        Args:
            name (str): The name of the Pokemon.
            facade (PygameFacade): The pygame facade.
            x (int): X position.
            y (int): Y position.
        Returns:
            None
        """
        super().__init__(name, facade, facade.load_image(random.choice(electric_paths), POKEMON_SIZE), x, y)

    def attack(self, other: 'Pokemon', mult: int = 1, div: float = 1) -> None:
        """
        Attacks another Pokemon, with penalty against Water type.

        Args:
            other (Pokemon): The target Pokemon.
            mult (int): Attack multiplier.
            div (float): Defense divisor.
        Returns:
            None
        """
        div = 1 * (not isinstance(other, WaterPokemon))
        return super().attack(other, div=div)
