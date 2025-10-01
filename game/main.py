from trainer import SmartTrainer
from world import World
from battle import Battle
from static.config import *


world = World(10, pygame_facade)
battle = Battle(5, 250, 60, pygame_facade)
running = True
trainers = [SmartTrainer("Данияр", pygame_facade, pygame_facade.load_image("game/static/images/trainer 1.png", TRAINER_SIZE), pygame_facade.load_image("game/static/images/trainer 11.png", TRAINER_SIZE), 10, 20),
            SmartTrainer("Тяночка", pygame_facade, pygame_facade.load_image("game/static/images/trainer 2.png", TRAINER_SIZE), pygame_facade.load_image("game/static/images/trainer 2.png", TRAINER_SIZE), 600, 20, True)]
flag = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            caught_pokemon = world.catch_pokemon(event.pos)
            if not caught_pokemon:
                world.add(event.pos)
            else:
                if trainers[0].ischoosing:
                    trainers[0].add(caught_pokemon)
                else:
                    trainers[1].add(caught_pokemon)
            trainers[0].ischoosing, trainers[1].ischoosing = trainers[1].ischoosing, trainers[0].ischoosing

    pygame_facade.clear_screen()

    if not (len(trainers[0].box) >= 5 and len(trainers[1].box) >= 5) and not flag:
        for trainer in trainers:
            trainer.draw()
        world.draw()
        world.update()
        pygame_facade.draw_text(250, 10, f'Выбирает: {trainers[0].name if trainers[0].ischoosing else trainers[1].name}', WHITE, 50)
    else:
        flag = True
        if not battle.started():
            battle.start(trainers[0], trainers[1])
        else:
            battle.update()
        battle.draw(pygame_facade.screen)

    pygame_facade.update_screen()
    pygame_facade.clock.tick(FPS)