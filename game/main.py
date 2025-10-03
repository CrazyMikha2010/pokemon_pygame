import pygame
from trainer import SmartTrainer
from world import World
from battle import Battle
from static.config import TRAINER_SIZE, FPS, WHITE, pygame_facade


world = World(10, pygame_facade)
battle = Battle(5, 250, 60, pygame_facade)
running = True
flag = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not world.catch_pokemon(event.pos):
                world.add(event.pos)
            
    pygame_facade.clear_screen()

    if not (len(world.trainer1.box) >= 5 and len(world.trainer2.box) >= 5) and not flag:
        world.trainer1.draw()
        world.trainer2.draw()
        world.draw()
        world.update()
        pygame_facade.draw_text(250, 10, f'Выбирает: {world.trainer1.name if world.trainer1.ischoosing else world.trainer2.name}', WHITE, 50)
    else:
        flag = True
        if not battle.started():
            battle.start(world.trainer1, world.trainer2)
        else:
            battle.update()
        battle.draw(pygame_facade.screen)

    pygame_facade.update_screen()
    pygame_facade.clock.tick(FPS)