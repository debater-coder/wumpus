from dataclasses import dataclass
import pickle
from typing import Literal


@dataclass
class LevelScore:
    """Stores the score achieved by completing a level."""

    deaths: int
    time: float


class Progress:
    """Utility class to handle saving and loading of high scores."""

    def __init__(self):
        self.load_progress()

    def load_progress(self):
        try:
            with open("progress.pickle", "rb") as fp:
                self.progress: dict[int, LevelScore] = pickle.load(fp)
        except FileNotFoundError:
            self.progress = {}

    def save_progress(self):
        with open("progress.pickle", "wb") as fp:
            pickle.dump(self.progress, fp)

    def get_high_score(self, level: int, score: LevelScore | None = None):
        """
        Returns the high score for a given level. If a score is provided, the high
        score will be updated if that score beats the current high score.
        """
        prev_high_score = self.progress.get(level)

        if not score:
            return prev_high_score

        if not prev_high_score:
            self.progress[level] = score
            self.save_progress()
            return score

        if score.deaths < prev_high_score.deaths:
            self.progress[level].deaths = score.deaths

        if score.time < prev_high_score.time:
            self.progress[level].time = score.time

        self.save_progress()
        return self.progress[level]

    def level_status(self, level: int) -> Literal["locked", "next", "completed"]:
        if self.progress.get(level):
            return "completed"

        for i in range(level):
            if not self.progress.get(i):
                return "locked"

        return "next"
