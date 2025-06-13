"""
11 Software Engineering 2025 Project
An implementation of the text adventure game "Hunt the Wumpus".
"""

import argparse
import random
import importlib.resources

from wumpus import Level
import wumpus.levels
from .player import TextPlayerController


parser = argparse.ArgumentParser(prog="Wumpus OOP")
parser.add_argument("-d", "--debug", action="store_true")
parser.add_argument("-s", "--seed")
args = parser.parse_args()
DEBUG = args.debug
SEED = args.seed


if SEED:
    random.seed(SEED)

level_map = importlib.resources.read_text(wumpus.levels, "01.json")
level = Level(level_map, debug=DEBUG)
player = TextPlayerController(level)

while True:
    if DEBUG:
        print("Level:", level)

    win = player.play()

    if win:
        print(f"AHA! You got the Wumpus. He was in room {level.get_wumpus_location()}")
        print("Wumpus will get you next time!")
    else:
        print("You lost!")

    if input("Play again (Y-N)? ")[0].lower() == "n":
        break

    if input("Same setup (Y-N)? ")[0].lower() == "n":
        level = Level(level_map, debug=DEBUG)
        player = TextPlayerController(level)
    else:
        player.respawn()
