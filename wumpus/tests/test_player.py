from random import seed
import unittest
from wumpus.level import Level
from wumpus.player import PlayerController
from wumpus.cave import Cave


class TestPlayerController(unittest.TestCase):
    """
    Black-box testing from the player's perspective. This test case does not
    test internal details such as event handling, instead testing from the
    PlayerController interface.
    """

    def setUp(self):
        with open("level.json") as fp:
            level_map = fp.read()
        seed("test")  # this ensures determinism
        self.level = Level(level_map)
        self.player = PlayerController(self.level)

    def test_spawn(self):
        self.assertListEqual(
            self.player.get_nearby_msgs(), ["I feel a draft.", "I smell a Wumpus."]
        )
        self.assertIsInstance(self.player.cave, Cave)
        self.assertEqual(self.player.cave.location, 18)
        self.assertListEqual(self.player.cave.tunnels, [9, 17, 19])

    def test_eaten(self):
        self.player.move(17)

        self.assertFalse(self.player.alive, "Player should be dead.")
        self.assertFalse(self.player.win, "Player should not have won.")

    def test_pit(self):
        self.player.move(9)
        self.assertFalse(self.player.alive, "Player should be dead.")
        self.assertFalse(self.player.win, "Player should not have won.")

        # respawn
        self.player.respawn()
        self.assertEqual(
            self.player.cave.location, 18, "Player should respawn in the same place."
        )

    def test_bats(self):
        self.player.move(19)
        self.player.move(11)
        self.player.move(10)
        self.player.move(2)

        # bats move player to random location
        self.assertEqual(self.player.cave.location, 5)

    def test_shoot_self(self):
        self.player.shoot([19, 18])
        self.assertFalse(self.player.alive, "Player should be dead.")
        self.assertFalse(self.player.win, "Player should not have won.")

    def test_shoot_wumpus(self):
        self.player.shoot([17])
        self.assertTrue(self.player.alive, "Player should be alive.")
        self.assertTrue(self.player.win, "Player should have won.")
