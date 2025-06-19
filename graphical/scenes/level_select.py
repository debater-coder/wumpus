from collections.abc import Iterator
import pygame as pg

from ..utils import button_up

from ..scene import PushScene, Scene, SceneEvent, SwitchScene
from ..colours import COLOURS
from ..gui import Button, VStack

from .playing import Playing


class LevelSelect(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["stone_900"])

        font = pg.font.Font(None, 64)

        self.buttons = [
            Button(pg.Rect(0, 0, 0, 80), f"Level {i}", font) for i in range(1, 6)
        ]
        self.stack = VStack(self.buttons, width=600, gap=20)

        self.back = Button(pg.Rect(40, 40, 300, 80), "Back", font)

    def update(self) -> Iterator[SceneEvent]:
        self.stack.rect.center = self.screen.get_rect().center
        self.stack.update()

        up = button_up()
        if self.back.update(up):
            from .menu import MainMenu

            yield SwitchScene(MainMenu(self.screen))

        updates = [button.update(up) for button in self.buttons]

        try:
            yield PushScene(Playing(self.screen, level_index=updates.index(True)))
        except ValueError:
            pass

    def paint(self):
        self.screen.blit(self.background, (0, 0))

        self.back.paint(self.screen)

        for button in self.buttons:
            button.paint(self.screen)

        pg.display.flip()

    def handle_pg_events(self):
        yield from self.update()
        self.paint()
