from dataclasses import dataclass
import pickle


@dataclass
class LevelScore:
    deaths: int
    time: float


class Progress:
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
