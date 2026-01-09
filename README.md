# Alien Invasion Game

A classic space shooter game built with Python and Pygame.

## Features
- Player-controlled spaceship
- Alien fleet with increasing difficulty
- Score system with high score tracking
- Lives system

## Requirements
- Python 3.x
- Pygame library

## Installation
```bash
pip install pygame
python alien_invasion.py
```

## Building Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --add-data "images;images" alien_invasion.py
```