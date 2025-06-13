from wumpus import Cave, PlayerController
from random import choice


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
    def play(self) -> bool:
        """Play the game, returns whether the game was won or lost."""
        while self.alive and not self.win:
            self.get_action()
        return self.win

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

                    locations = [locations[0]] + [
                        next_loc
                        if next_loc in (cave := self.level.get_cave(prev_loc)).tunnels
                        else choice(cave.tunnels)
                        for prev_loc, next_loc in zip(locations, locations[1:])
                    ]

                    self.shoot(locations)
                    break
                elif action.lower()[0] == "m":
                    location = input_location("Move to? ", self.level.level)
                    self.move(location)
                    break
            except ValueError:
                print("Can't do that!")
            else:
                print("Can't do that!")
