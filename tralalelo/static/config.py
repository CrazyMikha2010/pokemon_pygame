import pygame
import random
from pyfacade import *

water_paths = ["static/images/" + path + ".png" for path in ["image", "image copy"]]
fire_paths = ["static/images/" + path + ".png" for path in ["image copy 2", "image copy 3"]]
grass_paths = ["static/images/" + path + ".png" for path in ["image copy 4", "image copy 5"]]
electric_paths = ["static/images/" + path + ".png" for path in ["image copy 6", "image copy 7"]]

SCREEN_SIZE = (800, 500)
POKEMON_SIZE = (50, 80)
TRAINER_SIZE = (170, 500)

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

MAX_POKEMON_ATK = 5
MAX_POKEMON_DF = 5

FPS = 30

pygame_facade = PygameFacade(SCREEN_SIZE, "Mezh game")


