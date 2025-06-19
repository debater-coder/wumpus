from collections.abc import Iterator
import pygame as pg

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

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
