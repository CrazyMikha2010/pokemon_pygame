import pygame
from trainer import SmartTrainer
from world import World
from battle import Battle
from static.config import FPS, pygame_facade


world = World(10, pygame_facade)
battle = Battle(5, 250, 60, pygame_facade)
running = True
flag = False
show_restart = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if show_restart and battle.button_rect and battle.button_rect.collidepoint(event.pos):
                world = World(10, pygame_facade)
                battle = Battle(5, 250, 60, pygame_facade)
                show_restart = False
                flag = False
            elif not show_restart:
                if not world.catch_pokemon(event.pos):
                    world.add(event.pos)
            
    if not show_restart: pygame_facade.clear_screen()

    if not (len(world.trainer1.box) >= 5 and len(world.trainer2.box) >= 5) and not flag:
        world.draw()
        world.update()
    else:
        flag = True
        if not battle.started() and not show_restart:
            battle.start(world.trainer1, world.trainer2)
        elif not show_restart:
            battle.update()
            if len(battle.team1) == 0 or len(battle.team2) == 0:
                battle.end()
                show_restart = True
                
        if not show_restart: 
            battle.draw(pygame_facade.screen)
            pygame_facade.update_screen()
        

    pygame_facade.update_screen()
    pygame_facade.clock.tick(FPS)