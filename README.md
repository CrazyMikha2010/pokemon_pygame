# Pokemon Pygame 

A simple Pokemon battle game built with Python and Pygame. Catch, choose, and battle Pokemons with trainers in a graphical interface.

## Features
- Catch Pokemons by clicking on the world
- Choose your team and battle against another trainer
- Animated battle with health bars and turn-based attacks
- Restart the game with a button after a battle ends

## Requirements
- Python 3.8+
- Pygame

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/pokemon_pygame.git
   cd pokemon_pygame
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the game from the `game` directory:
```bash
python main.py
```

## Controls
- **Mouse click**: Catch a Pokemon or add a new one
- **Restart button**: Appears after a battle ends, click to restart
- **Quit**: Close the window or press the close button

## Testing
I didn't have any problems while developing the game

## OOP Patterns and methods I used
- **facade**: Pygame facade with its most common commands
- **static methods**: functions that don't require additional info within its class
- **property**: getters and setters for pokemon properties
- **singleton**: ensures only one instance of PygameFacade exists. I made it as decorator

Overall I tried to optimize the code as much as possible and split it into files

## Project Structure
```
pokemon_pygame/
├── game/
│   ├── main.py
│   ├── battle.py
│   ├── world.py
│   ├── trainer.py
│   ├── pokemon.py
│   ├── pyfacade.py
│   ├── static/
│   │   ├── colors.py
│   │   ├── config.py
│   │   └── images/
│   └── logs/
├── LICENSE
└── README.md
```

## Credits
- Sprites and images: Fandom pokemon Wiki
- Code: Mezhibovskiy Mikhail
- Teacher: Iljin Vladimir Vladimirovich

## License
MIT License