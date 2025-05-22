import unittest
import typing

from wumpus import hazards, cave, events


class TestWumpus(unittest.TestCase):
    def test_enter(self):
        final_locations = {0: 0, 1: 0, 2: 0, 3: 0}
        iterations = 1000

        for _ in range(iterations):
            wumpus = hazards.Wumpus({0: cave.Cave(0, [1, 2, 3])})
            wumpus.location = 0
            print(wumpus.location)

            enter_events = list(wumpus.on_player_enter())

            self.assertIsInstance(enter_events[0], events.PlayerKilled)

            if len(enter_events) > 1:
                self.assertEqual(len(enter_events), 2)
                self.assertIsInstance(enter_events[1], events.WumpusMoved)
                event = typing.cast(events.WumpusMoved, enter_events[1])

                self.assertIn(event.location, [1, 2, 3])
                final_locations[event.location] += 1
            else:
                self.assertEqual(len(enter_events), 1)
                final_locations[0] += 1

        self.assertAlmostEqual(final_locations[0] / iterations, 0.25, places=1)
        self.assertAlmostEqual(final_locations[1] / iterations, 0.25, places=1)
        self.assertAlmostEqual(final_locations[2] / iterations, 0.25, places=1)
        self.assertAlmostEqual(final_locations[3] / iterations, 0.25, places=1)
