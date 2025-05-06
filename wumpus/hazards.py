from __future__ import annotations
from typing import TYPE_CHECKING
from random import choice

if TYPE_CHECKING:
    from wumpus.level import Level
    from wumpus.player import PlayerController


class Hazard:
    """
    Hazards are located in a cave, they can affect the player's location or
    cause the player to lose.
    """
    def __init__(self, level: Level):
        self.location: int | None = None
        self.level = level

    def on_arrow_miss(self, player: PlayerController):
        """Called when an arrow does not hit any hazards that are not immune."""
        pass

    def on_arrow_enter(self, player: PlayerController) -> bool:
        """
        Called when an arrow hits the cave this hazard is in.

        Returns: Whether the arrow has considered to 'hit' the hazard.
        Most hazards are immune by arrows, so they should return False.
        """
        return False

    def on_player_enter(self, player: PlayerController):
        """Called when the player enters the cave this hazard is in."""
        pass

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

    def on_player_enter(self, player: PlayerController):
        player.alive = False
        player.win = False
        print("Wumpus EATS YOU UP!")
        self.startle(player)

    def on_arrow_enter(self, player: PlayerController) -> bool:
        player.win = True
        return True

    def on_arrow_miss(self, player: PlayerController):
        self.startle(player)

    def startle(self, player: PlayerController):
        if not self.location: raise ValueError

        move = choice([*self.level.get_cave(self.location).tunnels, None])

        if move:
            self.location = move

        if self.location == player.cave.location:
            player.alive = False
            player.win = False
            print("Wumpus EATS YOU UP!")



class BottomlessPit(Hazard):
    """Kills the player when it enters the cave."""
    def nearby_msg(self):
        return "I feel a draft."

    def on_player_enter(self, player: PlayerController):
        player.alive = False
        print("YIIIEEEE... fell in pit!")



class Superbats(Hazard):
    """
    Picks up the player and drops them in a random cave, potentially one
    with hazards.
    """
    def nearby_msg(self):
        return "Bats nearby."

    def on_player_enter(self, player: PlayerController):
        print("ZAP -- Super bat snatch! Elsewhereville for you!")
        player.move(choice(list(self.level.level.values())).location)
