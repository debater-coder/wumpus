from collections.abc import Iterator
import pygame as pg
import importlib.resources

from wumpus import Level
import wumpus.levels

from ..scene import PushScene, Scene, SceneEvent
from ..colours import COLOURS

from .paused import Paused


class Playing(Scene):
    def __init__(self, screen: pg.surface.Surface, level_index: int):
        self.screen = screen
        self.level_index = level_index

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

        font = pg.font.Font(None, 64)

        self.text = font.render(f"Level {level_index + 1}", True, COLOURS["zinc_50"])

        self.map = importlib.resources.read_text(wumpus.levels, f"{level_index:02}.json")
        self.level = Level(self.map)

    def update(self) -> Iterator[SceneEvent]:
        for event in pg.event.get(eventtype=pg.KEYUP):
            match event.key:
                case pg.K_ESCAPE:
                    yield PushScene(Paused(self.screen))

    def paint(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(
            self.text, self.text.get_rect(center=self.screen.get_rect().center)
        )


        for cave in (caves := self.level.level).values():
            for edge in cave.tunnels:
                pg.draw.line(self.screen, COLOURS["zinc_50"], pg.Vector2(caves[edge].coords) + pg.Vector2(1920, 1080) / 2, pg.Vector2(cave.coords) + pg.Vector2(1920, 1080) / 2)

        for cave in caves.values():
            pg.draw.circle(self.screen, COLOURS["zinc_900"], pg.Vector2(cave.coords) + pg.Vector2(1920, 1080) / 2, 50)

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
