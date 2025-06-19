from dataclasses import dataclass


@dataclass
class Cave:
    location: int
    tunnels: list[int]
    coords: tuple[float, float]
