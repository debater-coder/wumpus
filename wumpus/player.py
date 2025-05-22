from .events import ArrowShot, PlayerKilled, PlayerMoved, PlayerWon, Event
from .level import Level
from .cave import Cave

from random import choice
from typing import assert_never


class PlayerController:
    """
    Responsibility:
        - Emit events to level like PlayerMoved
        - Handle events such as PlayerKilled
    """

    def __init__(self, level: Level):
        self.level = level

        self.cave = level.choose_empty_cave()
        self.initial_cave = self.cave
        self.alive = True
        self.win = False

        self.emit_to_level(PlayerMoved(self.cave.location))

    def move(self, location: int):
        self.emit_to_level(PlayerMoved(location))

    def shoot(self, location: int):
        self.emit_to_level(ArrowShot(location))

    def emit_to_level(self, event: Event):
        for player_events in self.level.handle_event(event):
            match player_events:
                case PlayerKilled():
                    self.alive = False
                case PlayerWon():
                    self.win = True
                case PlayerMoved(location):
                    self.cave = self.level.get_cave(location)
                case _:
                    assert_never(player_events)

    def get_nearby_msgs(self):
        messages: list[str] = []

        for location in self.cave.tunnels:
            cave = self.level.get_cave(location)
            if hazard := self.level.get_hazard_in_cave(cave):
                messages.append(hazard.nearby_msg())

        return messages

    def get_action(self):
        raise NotImplementedError

    def play(self) -> bool:
        """Play the game, returns whether the game was won or lost."""
        while self.alive and not self.win:
            self.get_action()

        return self.win

    def respawn(self):
        self.cave = self.initial_cave
        self.alive = True
        self.win = False


def input_location(msg: str, level: dict[int, Cave]):
    while True:
        try:
            location = int(input(msg))
            if location in level:
                return location
        except ValueError:
            pass
        print("Can't go there!")


class TextPlayerController(PlayerController):
    def get_action(self):
        while True:
            print(f"You are in room {self.cave.location}.")
            for msg in self.get_nearby_msgs():
                print(f"    {msg}")
            print(
                f"Tunnels lead to {', '.join([str(tunnel) for tunnel in self.cave.tunnels])}."
            )

            action = input("Shoot or move (S-M)? ")
            try:
                if action.lower()[0] == "s":
                    rooms = int(input("No. of rooms? "))
                    if rooms < 1 or rooms > 5:
                        print("Crooked arrows aren't that crooked!")
                        continue

                    locations = [
                        input_location("Room #? ", self.level.level)
                        for _ in range(rooms)
                    ]

                    current_cave = self.cave

                    for location in locations:
                        if location not in current_cave.tunnels:
                            location = choice(current_cave.tunnels)
                            print("Lost control of arrow!")

                        self.shoot(location)

                        current_cave = self.level.get_cave(location)

                    break
                elif action.lower()[0] == "m":
                    location = input_location("Move to? ", self.level.level)
                    self.move(location)
                    break
            except ValueError:
                print("Can't do that!")
            else:
                print("Can't do that!")
