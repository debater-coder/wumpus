from collections.abc import Iterator
import pygame as pg
import importlib.resources

from wumpus import Level, PlayerController
from wumpus.hazards import Wumpus
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
        self.player = PlayerController(self.level)

        self.explored = {self.player.cave.location}
        self.wumpus_indicators: set[int] = set()

        self.renderer = Renderer(self.level, fov=90)
        self.renderer.focus_cave(self.player.cave)

        self.shooting_path: list[int] = []

    def handle_mouse_click(self, event: pg.event.Event):
        clicked_cave = self.renderer.get_cave_at_pos(pg.Vector2(event.pos))
        if clicked_cave is None:
            self.shooting_path = []
            return

        if event.button == 1:  # Left mouse button
            if clicked_cave.location in self.player.cave.tunnels:
                self.player.move(clicked_cave.location)
                self.renderer.focus_cave(self.player.cave)
                self.explored.add(self.player.cave.location)
                self.explored.add(clicked_cave.location)
        elif event.button == 3:  # Right mouse button
            if (
                not self.shooting_path
                and clicked_cave.location in self.player.cave.tunnels
            ):
                self.shooting_path.append(clicked_cave.location)
            elif (
                clicked_cave.location
                in self.level.get_cave(self.shooting_path[-1]).tunnels
            ):
                self.shooting_path.append(clicked_cave.location)
            else:
                self.shooting_path = []

    def respawn(self):
        self.player.respawn()
        self.renderer.focus_cave(self.player.cave)
        self.wumpus_indicators = set()

    def update(self) -> Iterator[SceneEvent]:
        for event in pg.event.get(eventtype=pg.KEYUP):
            match event.key:
                case pg.K_ESCAPE:
                    yield PushScene(Paused(self.screen))
                case pg.K_RETURN:
                    if self.shooting_path:
                        self.player.shoot(self.shooting_path)
                        self.shooting_path = []
                case pg.K_c:
                    self.shooting_path = []

        if not self.player.alive:
            # TODO: death screen
            yield PushScene(Paused(self.screen))
            self.respawn()

        if self.player.win:
            self.explored = set(self.level.level.keys())

        for location in self.player.cave.tunnels:
            if isinstance(
                self.level.get_hazard_in_cave(self.level.get_cave(location)), Wumpus
            ):
                self.wumpus_indicators.add(self.player.cave.location)

        for event in pg.event.get(eventtype=pg.MOUSEBUTTONUP):
            self.handle_mouse_click(event)

        for event in pg.event.get(eventtype=pg.MOUSEWHEEL):
            self.renderer.zoom(event.precise_y)

        for event in pg.event.get(eventtype=pg.MOUSEMOTION):
            if pg.mouse.get_pressed()[0]:
                if abs(event.rel[0]) > 0:
                    self.renderer.rotate(
                        self.renderer.basis_vectors[2][1]
                        ^ self.renderer.basis_vectors[0][1],
                        event.rel[0] / 1000,
                    )
                if abs(event.rel[1]) > 0:
                    self.renderer.rotate(
                        self.renderer.basis_vectors[2][1]
                        ^ self.renderer.basis_vectors[1][1],
                        event.rel[1] / 1000,
                    )

    def paint(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(
            self.text, self.text.get_rect(center=self.screen.get_rect().center)
        )

        self.renderer.paint(
            self.screen,
            self.player.cave.location,
            pg.Vector2(pg.mouse.get_pos()),
            self.shooting_path,
            self.explored,
            self.wumpus_indicators,
            self.player.win,
        )

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
