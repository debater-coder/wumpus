import unittest
import typing
import sys
import io

from wumpus import hazards, cave, events


class TestWumpus(unittest.TestCase):
    def test_enter(self):
        """Tests distribution of Wumpus movements"""
        suppress_text = io.StringIO()
        sys.stdout = suppress_text

        final_locations = {0: 0, 1: 0, 2: 0, 3: 0}
        iterations = 1000

        for _ in range(iterations):
            wumpus = hazards.Wumpus(
                {0: cave.Cave(0, [1, 2, 3])}
            )  # Wumpus spawns in cave 0
            wumpus.location = 0
            print(wumpus.location)

            enter_events = list(wumpus.on_player_enter())

            self.assertIsInstance(enter_events[0], events.PlayerKilled)
            self.assertIsInstance(enter_events[1], str)
            self.assertIn("EATS YOU UP", typing.cast(str, enter_events[1]))

            if len(enter_events) > 2:
                self.assertEqual(len(enter_events), 3)
                self.assertIsInstance(enter_events[2], events.WumpusMoved)
                event = typing.cast(events.WumpusMoved, enter_events[2])

                self.assertIn(event.location, [1, 2, 3])
                final_locations[event.location] += 1
            else:
                self.assertEqual(len(enter_events), 2)
                final_locations[0] += 1

        self.assertAlmostEqual(
            final_locations[0] / iterations, 0.25, places=1
        )  # 25% chance of not moving
        self.assertAlmostEqual(
            final_locations[1] / iterations, 0.25, places=1
        )  # 25% for each of the neighbouring caves
        self.assertAlmostEqual(final_locations[2] / iterations, 0.25, places=1)
        self.assertAlmostEqual(final_locations[3] / iterations, 0.25, places=1)

        sys.stdout = sys.__stdout__
