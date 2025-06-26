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

    def update(self) -> Iterator[SceneEvent]:
        for event in pg.event.get(eventtype=pg.KEYUP):
            match event.key:
                case pg.K_ESCAPE:
                    yield PushScene(Paused(self.screen))

    def perp_dist(self, coord: tuple[float, ...]):
        perpendicular = np.array(coord[2:])
        perpendicular[-1] += 5  # translate away from camera
        return math.sqrt(np.dot(perpendicular, perpendicular))

    def project(self, coord: tuple[float, ...]) -> pg.Vector2:
        """
        In persepective projection, the size of an object is based on
        its perependicuar distance to the camera. To project an arbitrary
        dimension vector we split it into its planar and perpendicular components.
        """
        planar = coord[:2]
        return (
            pg.Vector2(planar) * self.screen.get_rect().height / self.perp_dist(coord)
            + pg.Vector2(1920, 1080) / 2
        )

    def project_radius(self, radius: float, coord: tuple[float, ...]):
        return radius / self.perp_dist(coord)

    def paint(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(
            self.text, self.text.get_rect(center=self.screen.get_rect().center)
        )

        drawn = set()

        for cave in sorted(
            (caves := self.level.level).values(),
            key=lambda cave: self.perp_dist(cave.coords),
            reverse=True,
        ):
            for edge in cave.tunnels:
                if (cave.location, edge) in drawn:
                    continue
                pg.draw.line(
                    self.screen,
                    COLOURS["zinc_50"],
                    pg.Vector2(self.project(caves[edge].coords)),
                    pg.Vector2(self.project(cave.coords)),
                )
                drawn.add((edge, cave.location))

            print(self.perp_dist(cave.coords))
            pg.draw.circle(
                self.screen,
                pg.Color(COLOURS["amber_900"]).lerp(
                    (0, 0, 0, 0), max(0, min(0.5, self.perp_dist(cave.coords) / 2 - 2))
                ),
                pg.Vector2(self.project(cave.coords)),
                self.project_radius(100, cave.coords),
            )

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
