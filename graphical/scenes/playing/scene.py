from collections.abc import Iterator
import pygame as pg
import numpy as np
import math
import importlib.resources

from wumpus import Level
import wumpus.levels

from graphical.scene import PushScene, Scene, SceneEvent
from graphical.colours import COLOURS

from graphical.scenes.paused import Paused
from .renderer import Renderer


class Playing(Scene):
    def __init__(self, screen: pg.surface.Surface, level_index: int):
        self.screen = screen
        self.level_index = level_index

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

        font = pg.font.Font(None, 64)

        self.text = font.render(f"Level {level_index + 1}", True, COLOURS["zinc_600"])

        self.map = importlib.resources.read_text(
            wumpus.levels, f"{level_index:02}.json"
        )
        self.level = Level(self.map)

        self.renderer = Renderer(self.level, fov=90)

    def update(self) -> Iterator[SceneEvent]:
        for event in pg.event.get(eventtype=pg.KEYUP):
            match event.key:
                case pg.K_ESCAPE:
                    yield PushScene(Paused(self.screen))

        for event in pg.event.get(eventtype=pg.MOUSEWHEEL):
            self.renderer.zoom(event.precise_y)

    def paint(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(
            self.text, self.text.get_rect(center=self.screen.get_rect().center)
        )

        self.renderer.paint(self.screen)

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
