from collections.abc import Iterator
import typing
import pygame as pg
import importlib.resources

from graphical.animate import Animator
from graphical.progress import LevelScore
from graphical.scenes.win import Win
from wumpus import Level, PlayerController
from wumpus.hazards import Wumpus
import wumpus.levels

from graphical.scene import PushScene, Scene, SceneEvent, SwitchScene
from graphical.colours import COLOURS
from graphical.gui import Button

from graphical.utils import button_up

from graphical.scenes.paused import Paused
from .renderer import Renderer
import time


class Playing(Scene):
    def __init__(self, screen: pg.surface.Surface, level_index: int):
        self.screen = screen
        self.level_index = level_index
        self.clock = pg.time.Clock()
        self.start = time.time()
        # This saves the current timer whenever the level is paused, so the accumuated time
        # before the last pause is added to the final time.
        self.acc_time = 0

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

        self.font = pg.font.Font(None, 64)

        self.level_number_text = self.font.render(
            f"Level {level_index + 1}", True, COLOURS["zinc_600"]
        )

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
        self.deaths = 0
        self.update_deaths()

        self.death_tint = pg.Surface(self.screen.get_size())
        self.death_tint.fill(COLOURS["red_500"])

        self.death_fade: Animator | None = None

        self.pause_button = Button(pg.Rect(10, 10, 300, 80), "Pause", self.font)
        self.pause_button.bg_colour = COLOURS["blue_900"]
        self.pause_button.hover_colour = COLOURS["blue_800"]

    def start_death_fade(self):
        self.death_fade = Animator(127, 0, 500, self.end_death_fade)
        self.death_fade.start()

    def end_death_fade(self):
        self.death_fade = None

    def pause(self):
        self.acc_time += time.time() - self.start

    def resume(self):
        self.start = time.time()

    def update_deaths(self):
        self.death_text = self.font.render(
            f"Deaths: {self.deaths}", True, COLOURS["zinc_300"]
        )

    def handle_mouse_click(self, event: pg.event.Event):
        clicked_cave = self.renderer.get_cave_at_pos(pg.Vector2(event.pos))
        if clicked_cave is None:
            return

        if event.button == 1:  # Left mouse button
            if clicked_cave.location in self.player.cave.tunnels:
                self.player.move(clicked_cave.location)
                self.renderer.focus_cave(self.player.cave)
                self.explored.add(self.player.cave.location)
                self.explored.add(clicked_cave.location)
        elif event.button == 3 and len(self.shooting_path) < 5:  # Right mouse button
            if not self.shooting_path:
                if clicked_cave.location in self.player.cave.tunnels:
                    self.shooting_path.append(clicked_cave.location)
                    self.renderer.focus_cave(clicked_cave)
                else:
                    self.shooting_path = []
            else:
                if (
                    clicked_cave.location
                    in self.level.get_cave(self.shooting_path[-1]).tunnels
                ):
                    self.shooting_path.append(clicked_cave.location)
                    self.renderer.focus_cave(clicked_cave)
                else:
                    self.shooting_path = []

    def respawn(self):
        self.player.respawn()
        self.renderer.focus_cave(self.player.cave)
        self.wumpus_indicators = set()

    def update(self) -> Iterator[SceneEvent]:
        up = button_up()
        if self.pause_button.update(up):
            yield PushScene(Paused(self.screen))

        # Handle keypresses
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

        # Respawn and flash red on death
        if not self.player.alive:
            self.deaths += 1
            self.start_death_fade()
            self.update_deaths()
            self.respawn()

        if self.player.win:
            self.explored = set(self.level.level.keys())  # On win, all caves are explored
            yield SwitchScene(
                Win(
                    self.screen,
                    self.renderer,
                    self.level_index,
                    LevelScore(
                        deaths=self.deaths,
                        time=time.time() - self.start + self.acc_time,
                    ),
                )
            )

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
        delta = self.clock.tick(60)

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(
            self.level_number_text,
            self.level_number_text.get_rect(center=self.screen.get_rect().center),
        )
        self.screen.blit(
            self.death_text, self.death_text.get_rect(topright=(self.screen.get_rect().width - 40, 40))
        )

        self.renderer.paint(
            self.screen,
            self.player.cave.location,
            pg.Vector2(pg.mouse.get_pos()),
            self.shooting_path,
            self.explored,
            self.wumpus_indicators,
            self.player.win,
            delta=delta,
        )

        self.pause_button.paint(self.screen)

        if self.death_fade:
            self.death_fade.update(delta)

        # this is in a separate branch since update may cause the death fade to end
        if self.death_fade:
            self.death_tint.set_alpha(
                int(typing.cast(float, self.death_fade.get_value()))
            )
            self.screen.blit(self.death_tint, (0, 0))

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
