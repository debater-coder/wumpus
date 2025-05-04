"""
11 Software Engineering 2025 Project
An implementation of the text adventure game "Hunt the Wumpus".
"""
import argparse
from level import Level
from player import TextPlayerController


parser = argparse.ArgumentParser(prog='Wumpus OOP')
parser.add_argument('-d', '--debug', action='store_true')
DEBUG = parser.parse_args().debug


if __name__ == "__main__":
    with open("level.json") as fp:
        level_map = fp.read()

    level = Level(level_map)
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
            level = Level(level_map)
            player = TextPlayerController(level)
        else:
            player.respawn()
