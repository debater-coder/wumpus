from collections.abc import Iterator
import pygame as pg

from ..scene import PopScene, PushScene, Scene, SceneEvent, SwitchScene
from ..colours import COLOURS
from ..gui import Button, VStack
from ..utils import button_up

from .how_to_play import HowToPlay


class Paused(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen

        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["stone_900"])

        font = pg.font.Font(None, 64)

        self.buttons = [
            Button(pg.Rect(0, 0, 0, 80), "Resume Game", font),
            Button(pg.Rect(0, 0, 0, 80), "How to Play", font),
            Button(pg.Rect(0, 0, 0, 80), "Exit to Main Menu", font),
        ]
        self.stack = VStack(self.buttons, width=600, gap=20)

    def update(self) -> Iterator[SceneEvent]:
        self.stack.rect.center = self.screen.get_rect().center
        self.stack.update()

        up = button_up()
        resume, help, menu = [button.update(up) for button in self.buttons]

        if resume:
            yield PopScene()

        if help:
            yield PushScene(HowToPlay(self.screen))

        if menu:
            from .menu import MainMenu

            yield SwitchScene(MainMenu(self.screen))

    def paint(self):
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.paint(self.screen)

        pg.display.flip()

    def handle_pg_events(self) -> Iterator[SceneEvent]:
        yield from self.update()
        self.paint()
