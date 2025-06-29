import unittest
import wumpus.levels
import importlib.resources

from random import seed

from wumpus import Level, PlayerController, Cave


class TestPlayerController(unittest.TestCase):
    """
    Black-box testing from the player's perspective. This test case does not
    test internal details such as event handling, instead testing from the
    PlayerController interface.
    """

    def setUp(self):
        level_map = importlib.resources.read_text(wumpus.levels, "00.json")
        seed("test")  # this ensures determinism
        self.level = Level(level_map)
        self.player = PlayerController(self.level)

    def test_spawn(self):
        self.assertListEqual(self.player.get_nearby_msgs(), ["I feel a draft."])
        self.assertIsInstance(self.player.cave, Cave)
        self.assertEqual(self.player.cave.location, 17)
        self.assertListEqual(self.player.cave.tunnels, [3, 7, 11])

    def test_eaten(self):
        self.player.move(11)
        self.player.move(5)
        self.player.move(19)
        self.player.move(16)

        self.assertFalse(self.player.alive, "Player should be dead.")
        self.assertFalse(self.player.win, "Player should not have won.")

    def test_pit(self):
        self.player.move(7)
        self.assertFalse(self.player.alive, "Player should be dead.")
        self.assertFalse(self.player.win, "Player should not have won.")

        # respawn
        self.player.respawn()
        self.assertEqual(
            self.player.cave.location, 17, "Player should respawn in the same place."
        )

    def test_bats(self):
        self.player.move(11)
        self.player.move(1)

        # bats move player to random location
        self.assertEqual(self.player.cave.location, 4)

    def test_shoot_self(self):
        self.player.shoot([11, 17])
        self.assertFalse(self.player.alive, "Player should be dead.")
        self.assertFalse(self.player.win, "Player should not have won.")

    def test_shoot_wumpus(self):
        self.player.shoot([7, 19, 16])
        self.assertTrue(self.player.alive, "Player should be alive.")
        self.assertTrue(self.player.win, "Player should have won.")
