import pygame as pg
from ..scene import Scene
from ..gui.button import Button
from ..colours import COLOURS


class MainMenu(Scene):
    def __init__(self, screen: pg.surface.Surface):
        self.screen = screen
        font = pg.font.Font(None, 64)

        height = 100
        gap = 40
        top = gap
        width = 600
        self.buttons = [
            Button(pg.Rect(0, top, width, height), "Level Select", font),
            Button(pg.Rect(0, top + height + gap, width, height), "How to Play", font)
        ]

        # center buttons
        for button in self.buttons:
            button.rect.centerx = self.screen.get_rect().centerx


        self.background = pg.Surface(self.screen.get_size()).convert()
        self.background.fill(COLOURS["stone_900"])

    def update(self):
        for button in self.buttons:
            button.update()

    def paint(self):
        self.screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.paint(self.screen)

        pg.display.flip()

    def handle_pg_events(self, events: list[pg.event.Event]):
        self.update()
        self.paint()
        yield from []
