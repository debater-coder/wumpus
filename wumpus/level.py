from dataclasses import dataclass
import json
from wumpus.hazards import Hazard, BottomlessPit, Wumpus, Superbats
from random import choice


@dataclass
class Cave:
    location: int
    tunnels: list[int]



class Level:
    """A connected map of caves, as well as the locations of hazards."""
    def __init__(self, level_map: str):
        level = json.loads(level_map)
        self.level: dict[int, Cave] = {cave["location"]: Cave(cave["location"], cave["tunnels"]) for cave in level}
        self.hazards: dict[int, Hazard] = {}

        # Spawn 2 bottomless pits, 2 superbats and 1 Wumpus
        for hazard in [BottomlessPit(self), BottomlessPit(self), Superbats(self), Superbats(self), Wumpus(self)]:
            location = self.choose_empty_cave().location
            self.hazards[location] = hazard
            hazard.location = location

    def get_wumpus_location(self) -> int:
        cave = next((hazard for hazard in self.hazards.values() if isinstance(hazard, Wumpus))).location
        if not cave: raise ValueError
        return cave

    def choose_empty_cave(self) -> Cave:
        empty_caves = filter(lambda cave: cave.location not in self.hazards.keys(), self.level.values())
        return choice(list(empty_caves))

    def get_hazard_in_cave(self, cave: Cave) -> Hazard | None:
        return self.hazards.get(cave.location)

    def __repr__(self):
        return "\n".join(list(map(lambda cave: f"Cave {cave.location}, tunnels to {cave.tunnels}. Hazards: {self.get_hazard_in_cave(cave)}", self.level.values())))

    def get_cave(self, location: int) -> Cave:
        return self.level[location]
