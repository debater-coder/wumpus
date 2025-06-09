from collections.abc import Iterator
from random import choice
from .events import ArrowHit, Event, PlayerKilled, PlayerWon, WumpusMoved
from .cave import Cave
from .events import PlayerMoved


class Hazard:
    """
    Hazards are located in a cave, they can affect the player's location or
    cause the player to lose.
    """

    def __init__(self, level: dict[int, Cave]):
        self.location: int | None = None
        self.level = level

    def on_arrow_miss(self) -> Iterator[Event]:
        """Called when an arrow does not hit any hazards that are not immune."""
        yield from []

    def on_arrow_enter(self) -> Iterator[Event]:
        """
        Called when an arrow hits the cave this hazard is in.

        Returns: Whether the arrow has considered to 'hit' the hazard.
        Most hazards are immune by arrows, so they should return False.
        """
        yield from []

    def on_player_enter(self) -> Iterator[Event]:
        """Called when the player enters the cave this hazard is in."""
        yield from []

    def nearby_msg(self) -> str:
        """Returns a message to be printed when a hazard is nearby."""
        return "Unknown hazard nearby."


class Wumpus(Hazard):
    """
    The Wumpus dies when it is hit by an arrow, and is startled by arrows
    missing its cave or the player entering the cave. When it is startled,
    there is a 75% chance of it moving to another cave and a 25% chance of
    eating the player.
    """

    def nearby_msg(self):
        return "I smell a Wumpus."

    def on_player_enter(self):
        yield PlayerKilled()
        print("Wumpus EATS YOU UP!")
        yield from self.startle()

    def on_arrow_enter(self):
        yield ArrowHit()
        yield PlayerWon()

    def on_arrow_miss(self):
        yield from self.startle()

    def startle(self) -> Iterator[Event]:
        if self.location is None:
            raise Exception("Cannot startle Wumpus without location.")

        move = choice([*self.level[self.location].tunnels, None])

        if move:
            yield WumpusMoved(move)


class BottomlessPit(Hazard):
    """Kills the player when it enters the cave."""

    def nearby_msg(self):
        return "I feel a draft."

    def on_player_enter(self):
        print("You fell into a bottomless pit.")
        yield PlayerKilled()


class Superbats(Hazard):
    """
    Picks up the player and drops them in a random cave, potentially one
    with hazards.
    """

    def nearby_msg(self):
        return "Bats nearby."

    def on_player_enter(self):
        print("ZAP -- Super bat snatch! Elsewhereville for you!")
        yield PlayerMoved(choice(list(self.level.values())).location)
