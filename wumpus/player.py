from .events import (
    ArrowMissed,
    ArrowShot,
    PlayerKilled,
    PlayerMoved,
    PlayerWon,
    Event,
    ArrowHit,
)
from .level import Level
from .hazards import Hazard

from collections.abc import Iterator
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

        list(self.emit_to_level(PlayerMoved(self.cave.location)))

    def move(self, location: int):
        list(self.emit_to_level(PlayerMoved(location)))

    def shoot(self, locations: list[int]):
        for location in locations:
            if any(
                [
                    isinstance(event, ArrowHit)
                    for event in self.emit_to_level(ArrowShot(location))
                ]
            ):
                return

        self.emit_to_level(ArrowMissed())

    def emit_to_level(self, event: Event) -> Iterator[ArrowHit]:
        """Sends an event to the level, yielding events that happen in return."""
        for player_event in self.level.handle_event(event):
            if self.level.debug:
                print("player handling event:", player_event)
            match player_event:
                case PlayerKilled():
                    self.alive = False
                case PlayerWon():
                    self.win = True
                case PlayerMoved(location):
                    self.cave = self.level.get_cave(location)
                case ArrowHit():
                    yield player_event
                case str():
                    self.handle_msg(player_event)
                case _:
                    assert_never(player_event)

    def handle_msg(self, msg: str):
        pass

    def get_nearby_msgs(self):
        return [
            hazard.nearby_msg() for hazard in self.level.get_nearby_hazards(self.cave)
        ]

    def respawn(self):
        self.cave = self.initial_cave
        list(self.emit_to_level(PlayerMoved(self.cave.location)))
        self.alive = True
        self.win = False
