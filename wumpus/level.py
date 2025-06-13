import json
from random import choice
from collections.abc import Iterator
from typing import assert_never
from itertools import chain

from .events import (
    ArrowMissed,
    Event,
    PlayerKilled,
    PlayerWon,
    PlayerMoved,
    ArrowShot,
    ArrowHit,
    WumpusMoved,
)
from .hazards import Hazard, BottomlessPit, Superbats, Wumpus
from .cave import Cave


class Level:
    """A connected map of caves, as well as the locations of hazards."""

    def __init__(self, level_map: str, debug=False):
        self.debug = debug
        level = json.loads(level_map)
        self.level: dict[int, Cave] = {
            cave["location"]: Cave(cave["location"], cave["tunnels"]) for cave in level
        }
        self.hazards: dict[int, Hazard] = {}
        self.player: int | None = None

        # Spawn 2 bottomless pits, 2 superbats and 1 Wumpus
        for hazard in [
            BottomlessPit(self.level),
            BottomlessPit(self.level),
            Superbats(self.level),
            Superbats(self.level),
            Wumpus(self.level),
        ]:
            location = self.choose_empty_cave().location
            self.hazards[location] = hazard
            hazard.location = location

    def handle_event(
        self, event: Event
    ) -> Iterator[PlayerKilled | PlayerWon | PlayerMoved | ArrowHit | str]:
        """
        Handles an event triggered by an object in the game.

        Yields:
            - Events to be handled by the PlayerController
        """
        if self.debug:
            print(event)
        match event:
            case PlayerKilled() | PlayerWon() | ArrowHit():
                yield event  # these events are passed to the PlayerController
            case PlayerMoved(location):
                yield event

                self.player = location

                cave = self.get_cave(location)
                hazard = self.get_hazard_in_cave(cave)
                if self.debug:
                    print(f"handling player moved, hazard: {hazard}, cave: {cave}")
                if hazard:
                    yield from chain(
                        *(
                            self.handle_event(event)
                            for event in hazard.on_player_enter()
                        )
                    )

            case WumpusMoved(location):
                wumpus = self.get_hazard_in_cave(
                    self.get_cave(self.get_wumpus_location())
                )
                if not wumpus or not wumpus.location:
                    raise ValueError("no wumpus")

                # move the wumpus
                self.hazards[location] = wumpus
                del self.hazards[wumpus.location]
                wumpus.location = location

                # if we enter the room the player is in
                if wumpus.location == self.player:
                    yield from chain(
                        *(
                            self.handle_event(event)
                            for event in wumpus.on_player_enter()
                        )
                    )
            case ArrowShot(location):
                hazard = self.get_hazard_in_cave(self.get_cave(location))

                if location == self.player:
                    yield "Oops... You shot yourself!"
                    yield PlayerKilled()
                    return

                if hazard:
                    yield from chain(
                        *(
                            self.handle_event(event)
                            for event in chain(
                                *(
                                    hazard.on_arrow_enter()
                                    for hazard in self.hazards.values()
                                )
                            )
                        )
                    )
            case ArrowMissed():
                yield from chain(
                    *(
                        self.handle_event(event)
                        for event in chain(
                            *(
                                hazard.on_arrow_miss()
                                for hazard in self.hazards.values()
                            )
                        )
                    )
                )
            case str():
                yield event
            case _:
                assert_never(event)

    def get_wumpus_location(self) -> int:
        cave = next(
            (hazard for hazard in self.hazards.values() if isinstance(hazard, Wumpus))
        ).location
        if not cave:
            raise ValueError
        return cave

    def choose_empty_cave(self) -> Cave:
        empty_caves = filter(
            lambda cave: cave.location not in self.hazards.keys(), self.level.values()
        )
        return choice(list(empty_caves))

    def get_hazard_in_cave(self, cave: Cave) -> Hazard | None:
        return self.hazards.get(cave.location)

    def __repr__(self):
        return "\n".join(
            list(
                map(
                    lambda cave: f"Cave {cave.location}, tunnels to {cave.tunnels}. Hazards: {self.get_hazard_in_cave(cave)}",
                    self.level.values(),
                )
            )
        )

    def get_cave(self, location: int) -> Cave:
        return self.level[location]
