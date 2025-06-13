"""
Events are used to decouple the Hazards from the Level.
Instead of directly invoking methods on Level, Hazards yield Events, which
are dispatched to Level. This also prevents circular type imports between Level
and Hazards.
"""

from dataclasses import dataclass


type Event = (
    PlayerKilled
    | PlayerWon
    | PlayerMoved
    | WumpusMoved
    | ArrowShot
    | ArrowHit
    | ArrowMissed
    | str
)


@dataclass
class EntityMoved:
    location: int


class PlayerKilled:
    pass


class PlayerWon:
    pass


class PlayerMoved(EntityMoved):
    pass


class WumpusMoved(EntityMoved):
    pass


class ArrowShot(EntityMoved):
    pass


class ArrowHit:
    pass


class ArrowMissed:
    pass
