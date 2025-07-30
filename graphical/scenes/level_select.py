from collections.abc import Iterator
from typing import assert_never
import pygame as pg

from graphical.progress import Progress

from ..utils import button_up

from ..scene import PushScene, Scene, SceneEvent, SwitchScene
from ..colours import COLOURS
from ..gui import Button, VStack

from .playing import Playing


class LevelSelect(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["zinc_950"])

        font = pg.font.Font(None, 64)

        progress = Progress()
        progress.load_progress()

        self.buttons = []
        for i in range(5):
            status = progress.level_status(i)
            button = Button(pg.Rect(0, 0, 0, 80), f"Level {i + 1}" + (" (Locked)" if status == "locked" else ""), font)
            match status:
                case "completed":
                    pass
                case "next":
                    button.bg_colour = COLOURS["blue_900"]
                    button.hover_colour = COLOURS["blue_800"]
                case "locked":
                    button.bg_colour = COLOURS["zinc_900"]
                    button.hover_colour = COLOURS["zinc_900"]
                    button.text_colour = COLOURS["zinc_500"]
                case _:
                    assert_never(status)
            self.buttons.append(button)

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
        if not any(updates):
            return

        try:
            index = updates.index(True)
            progress = Progress()
            progress.load_progress()
            if progress.level_status(index) != "locked":
                yield PushScene(Playing(self.screen, level_index=index))
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
