from collections.abc import Iterator
import pygame as pg

from ..utils import button_up

from ..scene import PushScene, Scene, SceneEvent, SwitchScene

from .how_to_play import HowToPlay

from ..gui import Button, VStack

from ..colours import COLOURS

from .playing.renderer import Renderer

import importlib.resources
import wumpus.levels
from wumpus import Level


class MainMenu(Scene):
    """The main menu scene, with two buttons for a help menu and level selector."""

    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        font = pg.font.Font(None, 64)
        heading_font = pg.font.Font(None, 128)

        self.clock = pg.time.Clock()

        self.heading = heading_font.render("Wumpus: Network", True, COLOURS["zinc_50"])

        self.buttons = [
            Button(pg.Rect(0, 0, 0, 80), "Level Select", font),
            Button(pg.Rect(0, 0, 0, 80), "How to Play", font),
        ]
        self.stack = VStack(self.buttons, width=600, gap=20)

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

        # Random level for background interesting looking
        self.map = importlib.resources.read_text(wumpus.levels, "00.json")
        self.level = Level(self.map)
        self.renderer = Renderer(self.level, fov=90)

        # Black layer to fade out background
        self.fade_layer = pg.Surface(self.screen.get_size()).convert()
        self.fade_layer.fill((0, 0, 0))
        self.fade_layer.set_alpha(128)

    def update(self) -> Iterator[SceneEvent]:
        self.stack.rect.center = self.screen.get_rect().center
        self.stack.update()
        up = button_up()

        level_select, how_to_play = [button.update(up) for button in self.buttons]

        if level_select:
            from .level_select import LevelSelect

            yield SwitchScene(LevelSelect(self.screen))

        if how_to_play:
            yield PushScene(HowToPlay(self.screen))

    def paint(self):
        delta = self.clock.tick(60)
        self.screen.blit(self.background, (0, 0))

        self.renderer.rotate(
            self.renderer.basis_vectors[2][1] ^ self.renderer.basis_vectors[0][1],
            delta / 20000,
        )
        self.renderer.paint(
            self.screen, show_wumpus=True, explored=set(self.level.level.keys())
        )

        self.screen.blit(self.fade_layer, (0, 0))

        self.screen.blit(
            self.heading,
            self.heading.get_rect(centerx=self.screen.get_rect().centerx, y=300),
        )

        for button in self.buttons:
            button.paint(self.screen)

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
