from wumpus.level import Cave, Level
from random import choice

class PlayerController:
    def __init__(self, level: Level):
        self.level = level

        self.cave = level.choose_empty_cave()
        self.initial_cave = self.cave
        self.alive = True
        self.win = False

    def move(self, location: int):
        """Moves the player to the cave specified."""
        self.cave = self.level.get_cave(location)

        hazard = self.level.get_hazard_in_cave(self.cave)

        if hazard:
            hazard.on_player_enter(self)

    def shoot(self, location: int):
        """Shoots an arrow through the cave specified."""
        cave = self.level.get_cave(location)

        hazard = self.level.get_hazard_in_cave(cave)

        hit = hazard.on_arrow_enter(self) if hazard else False

        if not hit:
            # wake up any hazards that respond to arrow misses
            for hazard in self.level.hazards.values():
                hazard.on_arrow_miss(self)

        if location == self.cave.location:
            self.alive = False
            print("oops... you shot yourself!")

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
        except:
            pass
        print("Can't go there!")


class TextPlayerController(PlayerController):
    def get_action(self):
        while True:
            print(f"You are in room {self.cave.location}.")
            for msg in self.get_nearby_msgs():
                print(f"    {msg}")
            print(f"Tunnels lead to {', '.join([str(tunnel) for tunnel in self.cave.tunnels])}.")

            action = input("Shoot or move (S-M)? ")
            try:
                if action.lower()[0] == "s":
                    rooms = int(input("No. of rooms? "))
                    if rooms < 1 or rooms > 5:
                        print("Crooked arrows aren't that crooked!")
                        continue

                    locations = [input_location("Room #? ", self.level.level) for _ in range(rooms)]

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
            except:
                print("Can't do that!")
            else:
                print("Can't do that!")
