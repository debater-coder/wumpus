from collections.abc import Iterator
import pygame as pg

from ..scene import PushScene, Scene, SceneEvent, SwitchScene

from .how_to_play import HowToPlay
from .level_select import LevelSelect

from ..gui.button import Button
from ..gui.vstack import VStack

from ..colours import COLOURS


class MainMenu(Scene):
    """The main menu scene, with two buttons for a help menu and level selector."""
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        font = pg.font.Font(None, 64)

        self.buttons = [
            Button(pg.Rect(0, 0, 0, 80), "Level Select", font),
            Button(pg.Rect(0, 0, 0, 80), "How to Play", font),
        ]
        self.stack = VStack(self.buttons, width=600, gap=20)

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["stone_900"])

    def update(self) -> Iterator[SceneEvent]:
        self.stack.rect.center = self.screen.get_rect().center
        self.stack.update()

        level_select, how_to_play = [button.update() for button in self.buttons]

        if level_select:
            yield SwitchScene(LevelSelect(self.screen))

        if how_to_play:
            yield PushScene(HowToPlay(self.screen))

    def paint(self):
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.paint(self.screen)

        pg.display.flip()

    def handle_pg_events(self, events: list[pg.event.Event]):
        yield from self.update()
        self.paint()
